from fastapi.responses import JSONResponse
import util.mongodb_data_api as DocumentDB

def match_token_with_person_id(person_id: str, token: str):
    """
    All the check to the token is done here
    """
    if len(token) != 8:
        return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "malformed token"})
    db_query = DocumentDB.find_one(target_db=DocumentDB.DB_NAME, target_collection="TokenV1", find_filter={"token_id": token})
    print(db_query)
    if db_query is None:
        return JSONResponse(status_code=403, content={"status": "token not found"})
    if db_query["person_id"] != person_id:
        return JSONResponse(status_code=403, content={"status": "illegal request", "reason": "invalid token for this person_id"})
    return True