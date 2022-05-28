from pymongo.database import Database
from constant import AuthConfig
from datetime import datetime
import hashlib

import util.pymongo_wrapper as DocumentDB
from util import random_content
from util.custom_exception import TokenExpiredException
from constant import DBName


def get_person_id_with_token(pa_token: str, db_client: Database):
    """
    All the check to the token is done here
    Return an empty string any anything goes wrong or not matched
    """
    print(pa_token)
    if pa_token is None:
        return ""
    if len(pa_token) != AuthConfig.TOKEN_LENGTH:
        return ""
    db_query = DocumentDB.find_one(collection=DBName.TOKEN, find_filter={"token_value": pa_token}, db_client=db_client)
    print(db_query)
    if db_query is None:
        return ""
    if db_query["expiration_timestamp_int"] <= datetime.now().timestamp():
        deletion_query = DocumentDB.delete_one(collection=DBName.TOKEN, find_filter={"token_value": pa_token}, db_client=db_client)
        print(deletion_query)
        raise TokenExpiredException(db_query["token_value"], db_query["expiration_timestamp_int"])
    return db_query["person_id"]


def generate_pa_token_and_record(db_client: Database, person_id: str, token_lifespan: int):
    #  Assuming identity of the user already being testified
    while True:
        # Checking if the same token already being use
        # There is no do-while loop in Python
        generated_token = random_content.generate_access_token()
        current_checking_query = DocumentDB.find_one(collection=DBName.TOKEN,
                                                     find_filter={"token_value": generated_token},
                                                     db_client=db_client)
        if current_checking_query is None:
            break
    create_at = int(datetime.now().timestamp())
    expire_at = create_at + token_lifespan
    token_record_query = DocumentDB.insert_one(
        collection=DBName.TOKEN,
        document_body={
            "structure_version": 3,
            "person_id": person_id,
            "token_value": generated_token,
            "token_hash": hashlib.sha512(generated_token.encode("utf-8")).hexdigest(),
            "creation_timestamp_int": create_at,
            "expiration_timestamp_int": expire_at
        },
        db_client=db_client)
    print(token_record_query.inserted_id)
    #  In some scenario we want to return the expiration time to user
    return generated_token, expire_at
