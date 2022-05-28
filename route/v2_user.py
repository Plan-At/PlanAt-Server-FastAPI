# Builtin library
from datetime import datetime
import hashlib
import uuid

# Framework core library
from starlette.requests import Request
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

# Local file
from util import random_content, json_body
import util.pymongo_wrapper as DocumentDB
import util.json_filter as JSONFilter
from util.token_tool import get_person_id_with_token
from constant import AuthConfig, DBName

router = APIRouter()


@router.post("/create")
async def v2_create_user(request: Request, user_profile: json_body.UserProfileObject, password: str = Header(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = random_content.generate_person_id()
    full_profile = {
        "structure_version": 7,
        "person_id": person_id,
        "metadata": {
            "uuid": str(uuid.uuid4()),
            "seed": str(random_content.get_int(16)),
            "registration_timestamp_int": str(int(datetime.now().timestamp()))
        },
        "naming": {
            "unique_name": user_profile.naming.unique_name,
            "display_name_partial": user_profile.naming.display_name_partial,
            "display_name_full": user_profile.naming.display_name_full,
            "localization": [],
            "historical_name": []
        },
        "picture": {
            "avatar": {
                "image_id": user_profile.picture.avatar.image_id,
                "image_url": user_profile.picture.avatar.image_url
            },
            "background": {
                "image_id": user_profile.picture.background.image_id,
                "image_url": user_profile.picture.background.image_url
            }
        },
        "about": {
            "short_description": user_profile.about.short_description,
            "full_description": user_profile.about.full_description,
            "company_name": user_profile.about.company_name,
            "job_title": user_profile.about.job_title
        },
        "status": {
            "current_status": user_profile.status.current_status,
            "until": {
                "text": user_profile.status.until.text,
                "timestamp_int": user_profile.status.until.timestamp_int,
                "timezone_name": user_profile.status.until.timezone_name,
                "timezone_offset": user_profile.status.until.timezone_offset
            },
            "default_status": user_profile.status.default_status
        },
        "contact_method_collection": {
            "email_primary": {
                "domain_name": user_profile.contact_method_collection.email_primary.domain_name,
                "full_address": user_profile.contact_method_collection.email_primary.full_address
            },
            "phone": {
                "country_code": user_profile.contact_method_collection.phone.country_code,
                "regular_number": user_profile.contact_method_collection.phone.regular_number
            },
            "physical_address": {
                "full_address": user_profile.contact_method_collection.physical_address.full_address,
                "street_address": user_profile.contact_method_collection.physical_address.street_address,
                "city": user_profile.contact_method_collection.physical_address.city,
                "province": user_profile.contact_method_collection.physical_address.province,
                "country": user_profile.contact_method_collection.physical_address.country,
                "continent": user_profile.contact_method_collection.physical_address.continent,
                "post_code": user_profile.contact_method_collection.physical_address.post_code
            },
            "github": {
                "user_name": "",
                "user_handle": ""
            },
            "twitter": {
                "user_name": user_profile.contact_method_collection.twitter.user_name,
                "user_handle": user_profile.contact_method_collection.twitter.user_handle,
                "user_id": user_profile.contact_method_collection.twitter.user_id
            }
        }
    }
    profile_insert_query = DocumentDB.insert_one(db_client=db_client, collection=DBName.USER_PROFILE, document_body=full_profile)
    print(profile_insert_query.inserted_id)
    calendar_index_insert_query = DocumentDB.insert_one(db_client=db_client,
                                                        collection=DBName.CALENDAR_EVENT_INDEX,
                                                        document_body={"structure_version": 1, "person_id": person_id, "event_id_list": []})
    print(calendar_index_insert_query.inserted_id)
    login_credential_insert_query = DocumentDB.insert_one(db_client=db_client,
                                                          collection=DBName.LOGIN,
                                                          document_body={
                                                              "structure_version": 2,
                                                              "person_id": person_id,
                                                              "password_hash": hashlib.sha512(password.encode("utf-8")).hexdigest(),
                                                              "password_length": len(password),
                                                              "totp_status": "disabled",
                                                              "totp_secret_key": "",
                                                              "github_oauth_status": "disabled",
                                                              "github_email": ""
                                                          })
    print(login_credential_insert_query.inserted_id)
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "created", "person_id": person_id, "password": password})


@router.post("/delete")
async def v2_delete_user(request: Request, name_and_password: json_body.PasswordLoginBody):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = name_and_password.person_id
    credential_verify_query = DocumentDB.find_one(collection=DBName.LOGIN,
                                                  find_filter={"person_id": person_id},
                                                  db_client=db_client)
    print(credential_verify_query)
    # the hash string generated using hashlib is lowercase
    if hashlib.sha512(name_and_password.password.encode("utf-8")).hexdigest() != credential_verify_query["password_hash"]:
        return JSONResponse(status_code=403,
                            content={"status": "not found or not match",
                                     "person_id": name_and_password.person_id,
                                     "password": name_and_password.password})
    calendar_event_index_query = DocumentDB.find_one(db_client=db_client,
                                                     collection=DBName.CALENDAR_EVENT_INDEX,
                                                     find_filter={"person_id": person_id})
    calendar_event_count = 0
    if calendar_event_index_query is not None:
        calendar_event_index = calendar_event_index_query["event_id_list"]
        for each_calendar_event_id in calendar_event_index:
            calendar_event_count += DocumentDB.delete_one(db_client=db_client,
                                                          collection=DBName.CALENDAR_EVENT,
                                                          find_filter={"event_id": each_calendar_event_id}).deleted_count
    # Order based on the rank of importance and regenerate possibility
    token_count = DocumentDB.delete_many(db_client=db_client, collection=DBName.TOKEN, find_filter={"person_id": person_id}).deleted_count
    image_count = DocumentDB.delete_one(db_client=db_client, collection=DBName.IMAGE_HOSTING, find_filter={"person_id": person_id}).deleted_count
    collection_CalendarEventIndex = DocumentDB.delete_one(db_client=db_client, collection=DBName.CALENDAR_EVENT_INDEX, find_filter={"person_id": person_id}).deleted_count
    collection_User = DocumentDB.delete_one(db_client=db_client, collection=DBName.USER_PROFILE, find_filter={"person_id": person_id}).deleted_count
    collection_Login = DocumentDB.delete_one(db_client=db_client, collection=DBName.LOGIN, find_filter={"person_id": person_id}).deleted_count
    mongo_client.close()
    return JSONResponse(status_code=200,
                        content={"status": "everything bind to this person_id being deleted and unrecoverable",
                                 "deleted_token_count": token_count,
                                 "deleted_calendar_event_count": calendar_event_count,
                                 "deleted_image_count": image_count,
                                 "delete_calendar_event_index": collection_CalendarEventIndex == 1,
                                 "delete_user_profile": collection_User == 1,
                                 "delete_login_credential": collection_Login == 1})


@router.get("/id/get")
async def v2_get_user_id(request: Request, pa_token: str = Header(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = get_person_id_with_token(pa_token=pa_token, db_client=db_client)
    if person_id == "":
        mongo_client.close()
        return JSONResponse(status_code=403, content={"status": "user not found with this token", "pa_token": pa_token})
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "success", "person_id": person_id})


@router.get("/profile/get")
async def v2_get_user_profile(request: Request, person_id: str):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    if len(person_id) != AuthConfig.PERSON_ID_LENGTH:
        return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "malformed person_id"})
    db_query = DocumentDB.find_one(collection=DBName.USER_PROFILE, find_filter={"person_id": person_id}, db_client=db_client)
    if db_query is None:
        return JSONResponse(status_code=403, content={"status": "user not found"})
    mongo_client.close()
    return JSONFilter.universal_user_profile(input_json=db_query)


@router.post("/profile/name/update")
async def v2_update_user_profile_name(request: Request, req_body: json_body.NamingSection, pa_token: str = Header(None)):
    # All the update method of user profile is based on this
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = get_person_id_with_token(pa_token=pa_token, db_client=db_client)
    if person_id == "":
        mongo_client.close()
        return JSONResponse(status_code=403, content={"status": "user not found with this token", "pa_token": pa_token})
    # This based on assumption of structure version is matched
    # TODO: forbid special characters check if unique_name already being used
    update_query = DocumentDB.update_one(collection=DBName.USER_PROFILE,
                                         find_filter={"person_id": person_id},
                                         changes={"$set": {"naming.unique_name": req_body.unique_name,  # Need use "." to connect on nested object
                                                           "naming.display_name_full": req_body.display_name_full,
                                                           "naming.display_name_partial": req_body.display_name_partial},
                                                  "$push": {"naming.historical_name": req_body.display_name_full}},
                                         db_client=db_client)
    if update_query.matched_count != 1 and update_query.modified_count != 1:
        return JSONResponse(status_code=500,
                            content={"status": "failed to update",
                                     "matched_count": update_query.matched_count,
                                     "modified_count": update_query.modified_count})
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "success"})


@router.post("/profile/about/update")
async def v2_update_user_profile_about(request: Request, req_body: json_body.AboutSection, pa_token: str = Header(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = get_person_id_with_token(pa_token=pa_token, db_client=db_client)
    if person_id == "":
        mongo_client.close()
        return JSONResponse(status_code=403, content={"status": "user not found with this token", "pa_token": pa_token})
    # This based on assumption of structure version is matched
    # TODO: forbid special characters check length
    update_query = DocumentDB.update_one(collection=DBName.USER_PROFILE,
                                         find_filter={"person_id": person_id},
                                         changes={"$set": {"about.short_description": req_body.short_description,  # Need use "." to connect on nested object
                                                           "about.full_description": req_body.full_description,
                                                           "about.company_name": req_body.company_name,
                                                           "about.job_title": req_body.job_title}},
                                         db_client=db_client)
    if update_query.matched_count != 1 and update_query.modified_count != 1:
        return JSONResponse(status_code=500,
                            content={"status": "failed to update",
                                     "matched_count": update_query.matched_count,
                                     "modified_count": update_query.modified_count})
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "success"})


@router.post("/profile/status/update")
async def v2_update_user_profile_status(request: Request, req_body: json_body.StatusSection, pa_token: str = Header(None)):
    # Clone of previous two endpoint
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = get_person_id_with_token(pa_token=pa_token, db_client=db_client)
    if person_id == "":
        mongo_client.close()
        return JSONResponse(status_code=403, content={"status": "user not found with this token", "pa_token": pa_token})
    # This based on assumption of structure version is matched
    # TODO: check if the url passed in is a safe image
    update_query = DocumentDB.update_one(collection=DBName.USER_PROFILE,
                                         find_filter={"person_id": person_id},
                                         changes={"$set": {"status.current_status": req_body.current_status,  # Need use "." to connect on nested object
                                                           "status.until.text": req_body.until.text,
                                                           "status.until.timestamp_int": req_body.until.timestamp_int,
                                                           "status.until.timezone_name": req_body.until.timezone_name,
                                                           "status.until.timezone_offset": req_body.until.timezone_offset,
                                                           "status.default_status": req_body.default_status}},
                                         db_client=db_client)
    if update_query.matched_count != 1 and update_query.modified_count != 1:
        return JSONResponse(status_code=500,
                            content={"status": "failed to update",
                                     "matched_count": update_query.matched_count,
                                     "modified_count": update_query.modified_count})
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "success"})


@router.post("/profile/picture/update")
async def v2_update_user_profile_picture(request: Request, req_body: json_body.PictureSection, pa_token: str = Header(None)):
    # Clone of these previous three endpoint
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = get_person_id_with_token(pa_token=pa_token, db_client=db_client)
    if person_id == "":
        mongo_client.close()
        return JSONResponse(status_code=403, content={"status": "user not found with this token", "pa_token": pa_token})
    # This based on assumption of structure version is matched
    # TODO: check if the url passed in is a safe image
    update_query = DocumentDB.update_one(collection=DBName.USER_PROFILE,
                                         find_filter={"person_id": person_id},
                                         changes={"$set": {"picture.avatar.image_id": req_body.avatar.image_id,  # Need use "." to connect on nested object
                                                           "picture.avatar.image_url": req_body.avatar.image_url,
                                                           "picture.background.image_id": req_body.background.image_id,
                                                           "picture.background.image_url": req_body.background.image_url}},
                                         db_client=db_client)
    if update_query.matched_count != 1 and update_query.modified_count != 1:
        return JSONResponse(status_code=500,
                            content={"status": "failed to update",
                                     "matched_count": update_query.matched_count,
                                     "modified_count": update_query.modified_count})
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "success"})


# TODO: test this
@router.post("/profile/contact/update")
async def v2_update_user_profile_contact(request: Request, req_body: json_body.ContactMethodSection, pa_token: str = Header(None)):
    # Clone of these previous four endpoint
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    person_id = get_person_id_with_token(pa_token=pa_token, db_client=db_client)
    if person_id == "":
        mongo_client.close()
        return JSONResponse(status_code=403, content={"status": "user not found with this token", "pa_token": pa_token})
    # This based on assumption of structure version is matched
    # TODO: check if the url passed in is a safe image
    update_query = DocumentDB.update_one(collection=DBName.USER_PROFILE,
                                         find_filter={"person_id": person_id},
                                         changes={"$set": {"contact_method_collection.email_primary.domain_name": req_body.email_primary.domain_name,
                                                           "contact_method_collection.email_primary.full_address": req_body.email_primary.full_address,
                                                           "contact_method_collection.phone.country_code": req_body.phone.country_code,
                                                           "contact_method_collection.phone.regular_number": req_body.phone.regular_number,
                                                           "contact_method_collection.physical_address.full_address": req_body.physical_address.full_address,
                                                           "contact_method_collection.physical_address.street_address": req_body.physical_address.street_address,
                                                           "contact_method_collection.physical_address.city": req_body.physical_address.city,
                                                           "contact_method_collection.physical_address.province": req_body.physical_address.province,
                                                           "contact_method_collection.physical_address.country": req_body.physical_address.country,
                                                           "contact_method_collection.physical_address.continent": req_body.physical_address.continent,
                                                           "contact_method_collection.physical_address.post_code": req_body.physical_address.post_code,
                                                           "contact_method_collection.twitter.user_name": req_body.twitter.user_name,
                                                           "contact_method_collection.twitter.user_handle": req_body.twitter.user_handle,
                                                           "contact_method_collection.twitter.user_id": req_body.twitter.user_id,
                                                           "contact_method_collection.github.user_name": req_body.github.user_name,
                                                           "contact_method_collection.github.user_handle": req_body.github.user_handle}},
                                         db_client=db_client)
    if update_query.matched_count != 1 and update_query.modified_count != 1:
        return JSONResponse(status_code=500,
                            content={"status": "failed to update",
                                     "matched_count": update_query.matched_count,
                                     "modified_count": update_query.modified_count})
    mongo_client.close()
    return JSONResponse(status_code=200, content={"status": "success"})
