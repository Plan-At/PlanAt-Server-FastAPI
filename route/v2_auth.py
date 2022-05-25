# Builtin library
from datetime import datetime
import hashlib
import aiohttp

# Framework core library
import requests
from starlette.requests import Request
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
import pyotp

# Local file
from util import random_content, json_body
import util.pymongo_wrapper as DocumentDB

router = APIRouter()


@router.post("/token/revoke", tags=["V2"])
async def v2_revoke_auth_token(request: Request, pa_token: str = Header(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    token_deletion_query = DocumentDB.delete_one(
        collection="TokenV3",
        find_filter={"token_value": pa_token},
        db_client=db_client)
    mongo_client.close()
    if token_deletion_query is None:
        return JSONResponse(status_code=500, content={"status": "failed to remove the old token to database", "pa_token": pa_token})
    elif token_deletion_query.deleted_count == 0:
        return JSONResponse(status_code=404, content={"status": "token not found", "pa_token": pa_token})
    elif token_deletion_query.deleted_count == 1:
        return JSONResponse(status_code=200, content={"status": "deleted", "pa_token": pa_token})


@router.post("/password/verify", tags=["V2"])
async def v2_verify_auth_password(request: Request, cred: json_body.PasswordLoginBody):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    credential_verify_query = DocumentDB.find_one(collection="LoginV1",
                                                  find_filter={"person_id": cred.person_id},
                                                  db_client=db_client)
    print(credential_verify_query)
    # the hash string generated using hashlib is lowercase
    if (credential_verify_query is None) or not (
            hashlib.sha512(cred.password.encode("utf-8")).hexdigest() == credential_verify_query["password_hash"]):
        mongo_client.close()
        return JSONResponse(status_code=403,
                            content={"status": "not found or not match",
                                     "person_id": cred.person_id,
                                     "password": cred.password})
    while True:
        # Checking if the same token already being use
        # There is no do-while loop in Python
        generated_token = random_content.generate_access_token()
        current_checking_query = DocumentDB.find_one(collection="TokenV1",
                                                     find_filter={"token_value": generated_token},
                                                     db_client=db_client)
        if current_checking_query is None:
            break
    create_at = int(datetime.now().timestamp())
    expire_at = create_at + cred.token_lifespan
    token_record_query = DocumentDB.insert_one(
        collection="TokenV3",
        document_body={
            "structure_version": 3,
            "person_id": cred.person_id,
            "token_value": generated_token,
            "token_hash": hashlib.sha512(generated_token.encode("utf-8")).hexdigest(),
            "creation_timestamp_int": create_at,
            "expiration_timestamp_int": expire_at
        },
        db_client=db_client)
    if token_record_query is None:
        return JSONResponse(status_code=500,
                            content={"status": "token generated but failed to insert that token to database"})
    mongo_client.close()
    return JSONResponse(status_code=200,
                        content={"status": "success", "pa_token": generated_token, "expiration_timestamp": expire_at})


# TODO: revoke existing session/token
@router.post("/password/update", tags=["V2"])
async def v2_update_auth_password(request: Request, old_cred: json_body.PasswordLoginBody, new_cred: json_body.PasswordLoginBody):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    credential_verify_query = DocumentDB.find_one(collection="LoginV1",
                                                  find_filter={"person_id": old_cred.person_id},
                                                  db_client=db_client)
    print(credential_verify_query)
    # verify the old password
    if (credential_verify_query is None) or not (
            hashlib.sha512(old_cred.password.encode("utf-8")).hexdigest() == credential_verify_query["password_hash"]):
        mongo_client.close()
        return JSONResponse(status_code=403,
                            content={"status": "not found or not match",
                                     "person_id": old_cred.person_id,
                                     "password": old_cred.password})
    new_credential_entry = {
        "structure_version": 1,
        "person_id": old_cred.person_id,
        "password_hash": hashlib.sha512(new_cred.password.encode("utf-8")).hexdigest(),
        "password_length": len(new_cred.password),
    }
    credential_update_query = DocumentDB.replace_one(collection="LoginV1",
                                                     find_filter={"person_id": old_cred.person_id},
                                                     document_body=new_credential_entry,
                                                     db_client=db_client)
    print(credential_update_query)
    if credential_update_query.matched_count != 1 and credential_update_query.modified_count != 1:
        # trying to make the break in the first place, if no error might proceed to other steps
        return JSONResponse(status_code=500, content={"status": "failed to update",
                                                      "person_id": old_cred.person_id,
                                                      "password": old_cred.password})
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "success", "voided": old_cred.password})


@router.post("/totp/enable", tags=["V2"])
async def v2_enable_auth_totp(request: Request, cred: json_body.PasswordLoginBody):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    # same as the traditional plain-password login
    credential_verify_query = DocumentDB.find_one(collection="LoginV1",
                                                  find_filter={"person_id": cred.person_id},
                                                  db_client=db_client)
    print(credential_verify_query)
    if (credential_verify_query is None) or not (
            hashlib.sha512(cred.password.encode("utf-8")).hexdigest() == credential_verify_query["password_hash"]):
        mongo_client.close()
        return JSONResponse(status_code=403,
                            content={"status": "not found or not match",
                                     "person_id": cred.person_id,
                                     "password": cred.password})
    if credential_verify_query["totp_status"] != "disabled":
        return JSONResponse(status_code=200,
                            content={"status": "Time-based OTP already enabled for this user",
                                     "person_id": cred.person_id})
    new_secret_key = pyotp.random_base32()
    authenticator_text = url = pyotp.totp.TOTP(new_secret_key).provisioning_uri(name=cred.person_id,
                                                                                issuer_name='Plan-At')


@router.post("/totp/disable", tags=["V2"])
async def v2_disable_auth_totp():
    # Copy and Paste of /enable
    pass


@router.post("/totp/verify", tags=["V2"])
async def v2_verify_auth_totp():
    pass


@router.post("/github/enable", tags=["V2"])
async def v2_enable_auth_github(request: Request, req_body: json_body.GitHubOAuthCode, pa_token: str = Header(None)):
    github_session = aiohttp.ClientSession()
    a = await github_session.post(f"https://github.com/login/oauth/access_token?client_id={1}&client_secret={2}&code={3}")
    print(a.status, a.text())
    a = a.json()
    return JSONResponse(status_code=200, content={"status": "success", "code": req_body.code})


@router.post("/github/disable", tags=["V2"])
async def v2_disable_auth_github(request: Request, req_body: json_body.GitHubOAuthCode, pa_token: str = Header(None)):
    pass


@router.post("/github/verify", tags=["V2"])
async def v2_verify_auth_github(request: Request, req_body: json_body.GitHubOAuthCode):
    pass


