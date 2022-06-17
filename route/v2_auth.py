# Builtin library
import hashlib
import json
from urllib.parse import parse_qs
import aiohttp

# Framework core library
from starlette.requests import Request
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
import pyotp

# Local file
from util import json_body, token_tool
import util.pymongo_wrapper as DocumentDB
from constant import DBName

router = APIRouter()

TOKEN = json.load(open("app.token.json", encoding="utf-8"))

@router.post("/token/revoke")
async def v2_revoke_auth_token(request: Request, pa_token: str = Header(None)):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    token_deletion_query = DocumentDB.delete_one(
        collection=DBName.TOKEN,
        find_filter={"token_value": pa_token},
        db_client=db_client)
    mongo_client.close()
    if token_deletion_query is None:
        return JSONResponse(status_code=500,
                            content={"status": "failed to remove the old token to database", "pa_token": pa_token})
    elif token_deletion_query.deleted_count == 0:
        return JSONResponse(status_code=404, content={"status": "token not found", "pa_token": pa_token})
    elif token_deletion_query.deleted_count == 1:
        return JSONResponse(status_code=200, content={"status": "deleted", "pa_token": pa_token})


@router.post("/password/verify")
async def v2_verify_auth_password(request: Request, cred: json_body.PasswordLoginBody):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    credential_verify_query = DocumentDB.find_one(collection=DBName.LOGIN,
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
    generated_token = token_tool.generate_pa_token_and_record(db_client=db_client,
                                                              person_id=cred.person_id,
                                                              token_lifespan=cred.token_lifespan)
    mongo_client.close()
    return JSONResponse(status_code=200,
                        content={"status": "success",
                                 "pa_token": generated_token[0],
                                 "expiration_timestamp": generated_token[1]})


# TODO: revoke existing session/token
@router.post("/password/update")
async def v2_update_auth_password(request: Request, old_cred: json_body.PasswordLoginBody, new_cred: json_body.PasswordLoginBody):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    credential_verify_query = DocumentDB.find_one(collection=DBName.LOGIN,
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
    credential_update_query = DocumentDB.replace_one(collection=DBName.LOGIN,
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


@router.post("/totp/enable")
async def v2_enable_auth_totp(request: Request, cred: json_body.PasswordLoginBody):
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    # same as the traditional plain-password login
    credential_verify_query = DocumentDB.find_one(collection=DBName.LOGIN,
                                                  find_filter={"person_id": cred.person_id},
                                                  db_client=db_client)
    print(credential_verify_query)
    if (credential_verify_query is None) \
            or (hashlib.sha512(cred.password.encode("utf-8")).hexdigest() != credential_verify_query["password_hash"]):
        mongo_client.close()
        return JSONResponse(status_code=403,
                            content={"status": "user not found or not match",
                                     "person_id": cred.person_id,
                                     "password": cred.password})
    if credential_verify_query["totp_status"] != "disabled":
        mongo_client.close()
        return JSONResponse(status_code=200,
                            content={"status": "Time-based OTP already enabled for this user",
                                     "person_id": cred.person_id})
    new_secret_key = pyotp.random_base32()
    authenticator_url = pyotp.totp.TOTP(new_secret_key).provisioning_uri(name=cred.person_id,
                                                                         issuer_name='Plan-At')
    credential_modify_query = DocumentDB.update_one(db_client=db_client,
                                                    collection=DBName.LOGIN,
                                                    find_filter={"person_id": cred.person_id},
                                                    changes={"$set": {"totp_status": "enabled",
                                                                      "totp_secret_key": new_secret_key}})
    if credential_modify_query.matched_count != 1 and credential_modify_query.modified_count != 1:
        return JSONResponse(status_code=500, content={"status": "failed to register the secret_key for totp in database",
                                                      "matched_count": credential_modify_query.matched_count,
                                                      "modified_count": credential_modify_query.modified_count})
    mongo_client.close()
    return JSONResponse(status_code=200,
                        content={"status": "Time-based OTP enabled for this user",
                                 "person_id": cred.person_id,
                                 "authenticator_url": authenticator_url})


@router.post("/totp/disable")
async def v2_disable_auth_totp(request: Request, cred: json_body.PasswordLoginBody):
    # Copy and Paste of /enable
    # Not require current output from Authenticator since the user might lose their
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    # same as the traditional plain-password login
    credential_verify_query = DocumentDB.find_one(collection=DBName.LOGIN,
                                                  find_filter={"person_id": cred.person_id},
                                                  db_client=db_client)
    print(credential_verify_query)
    if (credential_verify_query is None) \
            or (hashlib.sha512(cred.password.encode("utf-8")).hexdigest() != credential_verify_query["password_hash"]):
        mongo_client.close()
        return JSONResponse(status_code=403,
                            content={"status": "user not found or not match",
                                     "person_id": cred.person_id,
                                     "password": cred.password})
    #  checking current totp status
    if credential_verify_query["totp_status"] != "enabled":
        mongo_client.close()
        return JSONResponse(status_code=200,
                            content={"status": "Time-based OTP not enabled for this user",
                                     "person_id": cred.person_id})
    credential_modify_query = DocumentDB.update_one(db_client=db_client,
                                                    collection=DBName.LOGIN,
                                                    find_filter={"person_id": cred.person_id},
                                                    changes={"$set": {"totp_status": "disabled",
                                                                      "totp_secret_key": ""}})
    if credential_modify_query.matched_count != 1 and credential_modify_query.modified_count != 1:
        return JSONResponse(status_code=500,
                            content={"status": "failed to delete existing secret_key for totp in database",
                                                      "matched_count": credential_modify_query.matched_count,
                                                      "modified_count": credential_modify_query.modified_count})
    mongo_client.close()
    return JSONResponse(status_code=200,
                        content={"status": "Time-based OTP disabled for this user",
                                 "person_id": cred.person_id})


@router.post("/totp/verify")
async def v2_verify_auth_totp(request: Request, person_id: str, totp_code: str):
    # Copy and Paste of /disable
    # Not require current output from Authenticator since the user might lose their
    mongo_client = DocumentDB.get_client()
    db_client = mongo_client.get_database(DocumentDB.DB)
    # if len(str(int(totp_code))) != 6:  # also verify if its actual int but not working if start with zero
    if len(totp_code) != 6:  # also verify if its actual int but not working if start with zero
        return JSONResponse(status_code=400,
                            content={"status": "totp_code malformed",
                                     "totp_code": totp_code})
    # same as the traditional plain-password login
    credential_verify_query = DocumentDB.find_one(collection=DBName.LOGIN,
                                                  find_filter={"person_id": person_id},
                                                  db_client=db_client)
    print(credential_verify_query)
    if credential_verify_query is None:
        mongo_client.close()
        return JSONResponse(status_code=403,
                            content={"status": "user not found or totp_code not match",
                                     "person_id": person_id,
                                     "totp_code": totp_code})
    #  Checking current totp status
    if credential_verify_query["totp_status"] != "enabled":
        mongo_client.close()
        return JSONResponse(status_code=200,
                            content={"status": "Time-based OTP not enabled for this user",
                                     "person_id": person_id})

    if not pyotp.TOTP(credential_verify_query["totp_secret_key"]).verify(totp_code):
        mongo_client.close()
        return JSONResponse(status_code=403,
                            content={"status": "user not found or totp_code not match",
                                     "person_id": person_id,
                                     "totp_code": totp_code})
    generated_token = token_tool.generate_pa_token_and_record(db_client=db_client,
                                                              person_id=person_id,
                                                              token_lifespan=(60 * 60 * 24 * 1))
    mongo_client.close()
    return JSONResponse(status_code=200,
                        content={"status": "success",
                                 "person_id": person_id,
                                 "pa_token": generated_token[0],
                                 "expiration_timestamp": generated_token[1]})


@router.post("/github/enable")
async def v2_enable_auth_github(request: Request, req_body: json_body.GitHubOAuthCode, pa_token: str = Header(None)):
    github_session = aiohttp.ClientSession()
    to_url = f"https://github.com/login/oauth/access_token?client_id={TOKEN['github_oauth']['client_id']}&client_secret={TOKEN['github_oauth']['client_secret']}&code={req_body.code}"
    resp1 = await github_session.post(to_url)
    print(resp1.status, resp1.headers)  # just the attributes of the response object so no need to wait again
    print(parse_qs(await resp1.text()))
    await github_session.close()  # must close the session otherwise will throw warning
    return JSONResponse(status_code=200, content={"status": "success", "code": req_body.code})


@router.post("/github/disable")
async def v2_disable_auth_github(request: Request, req_body: json_body.GitHubOAuthCode, pa_token: str = Header(None)):
    pass


@router.post("/github/verify")
async def v2_verify_auth_github(request: Request, req_body: json_body.GitHubOAuthCode):
    pass
