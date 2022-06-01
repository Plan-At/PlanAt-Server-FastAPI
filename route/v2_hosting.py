import json

from starlette.requests import Request
from fastapi import APIRouter, File, Header, Form, UploadFile
from fastapi.responses import JSONResponse

import util.pymongo_wrapper as DocumentDB
from util.token_tool import get_person_id_with_token
from util import image4io
from constant import ServerConfig, ContentLimit, DBName

router = APIRouter()


@router.post("/image/upload")
async def v2_upload_image(request: Request, image_file_bytes: bytes = File(..., max_length=ContentLimit.IMAGE_SIZE), pa_token: str = Header(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = get_person_id_with_token(pa_token, db_client)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "you need to upload an image", "pa_token": pa_token})
    assigned_id = image4io.generate_file_id(local_file_bytes=image_file_bytes)
    resp = image4io.uploadImage(
        authorization=image4io.calculate_basic_auth(
            api_key=json.load(open("app.token.json"))["image4io"]["api_key"],
            api_secret=json.load(open("app.token.json"))["image4io"]["api_secret"]),
        local_file_bytes=image_file_bytes,
        local_file_name=assigned_id,  # No need to specify the file extension here, this external hosting service will decide based on the actual image
        remote_folder_path=ServerConfig.IMAGEBED_FOLDER)
    if resp.status_code != 200:
        return JSONResponse(status_code=500, content={"status": "image upload failed", "reason": resp.json()["errors"]})
    image_info = resp.json()
    print(image_info)
    report_card = {
        "structure_version": 2,
        "person_id": person_id,
        "image_url": image_info["uploadedFiles"][0]["url"],
        "image_id": assigned_id,
        "image_file_name": image_info["uploadedFiles"][0]["userGivenName"],
        "image_file_path": image_info["uploadedFiles"][0]["name"],
        "image_size": image_info["uploadedFiles"][0]["size"],
        "image_width": image_info["uploadedFiles"][0]["width"],
        "image_height": image_info["uploadedFiles"][0]["height"],
        "hosting_provider": "image4io"
    }
    db_action_result = DocumentDB.insert_one(collection=DBName.IMAGE_HOSTING, document_body=report_card, db_client=db_client)
    print(db_action_result)
    mongo_client.close()
    return JSONResponse(status_code=201,
                        content={"status": "success", "image_id": assigned_id, "image_url": image_info["uploadedFiles"][0]["url"]})


@router.post("/image/delete")
async def v2_delete_image(request: Request, image_id: str, pa_token: str = Header(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = get_person_id_with_token(pa_token, db_client)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "you need to upload an image", "pa_token": pa_token})
    image_info_query = DocumentDB.find_one(collection=DBName.IMAGE_HOSTING, find_filter={"image_id": image_id}, db_client=db_client)
    print(image_info_query)
    resp = image4io.deleteImage(
        authorization=image4io.calculate_basic_auth(
            api_key=json.load(open("app.token.json"))["image4io"]["api_key"],
            api_secret=json.load(open("app.token.json"))["image4io"]["api_secret"]),
        remote_file_path=image_info_query["image_file_path"]
    )
    if resp.status_code != 200:
        return JSONResponse(status_code=500, content={"status": "image deletion failed", "reason": resp.json()["errors"]})
    image_info = resp.json()
    print(image_info)
    db_action_result = DocumentDB.delete_one(collection=DBName.IMAGE_HOSTING, find_filter={"image_id": image_id}, db_client=db_client)
    if db_action_result.deleted_count != 1:
        return JSONResponse(status_code=500,
                            content={"status": "image deleted from hosting service but failed to remove relevant record from our database", "image_id": image_id})
    mongo_client.close()
    return JSONResponse(status_code=201,
                        content={"status": "deleted", "image_id": image_id})


@router.post("/image/form_upload")
async def v2_form_upload_image(request: Request, image_file: UploadFile = Form(None), pa_token: str = Form(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    image_file = await image_file.read()
    person_id = get_person_id_with_token(pa_token, db_client)
    if person_id == "":
        return JSONResponse(status_code=403, content={"status": "you need to upload an image", "pa_token": pa_token})
    assigned_id = image4io.generate_file_id(local_file_bytes=image_file)
    resp = image4io.uploadImage(
        authorization=image4io.calculate_basic_auth(
            api_key=json.load(open("app.token.json"))["image4io"]["api_key"],
            api_secret=json.load(open("app.token.json"))["image4io"]["api_secret"]),
        local_file_bytes=image_file,
        local_file_name=assigned_id,  # No need to specify the file extension here, this external hosting service will decide based on the actual image
        remote_folder_path=ServerConfig.IMAGEBED_FOLDER)
    if resp.status_code != 200:
        return JSONResponse(status_code=500, content={"status": "image upload failed", "reason": resp.json()["errors"]})
    image_info = resp.json()
    print(image_info)
    report_card = {
        "structure_version": 2,
        "person_id": person_id,
        "image_url": image_info["uploadedFiles"][0]["url"],
        "image_id": assigned_id,
        "image_file_name": image_info["uploadedFiles"][0]["userGivenName"],
        "image_file_path": image_info["uploadedFiles"][0]["name"],
        "image_size": image_info["uploadedFiles"][0]["size"],
        "image_width": image_info["uploadedFiles"][0]["width"],
        "image_height": image_info["uploadedFiles"][0]["height"],
        "hosting_provider": "image4io"
    }
    db_action_result = DocumentDB.insert_one(collection=DBName.IMAGE_HOSTING, document_body=report_card, db_client=db_client)
    print(db_action_result)
    mongo_client.close()
    return JSONResponse(status_code=201,
                        content={"status": "success", "image_id": assigned_id, "image_url": image_info["uploadedFiles"][0]["url"]})
