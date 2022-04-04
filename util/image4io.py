import base64
import hashlib
import json
import requests
from datetime import datetime

def calculate_basic_auth(api_key: str, api_secret: str):
    return base64.b64encode(f"{api_key}:{api_secret}".encode("ascii")).decode("ascii")

def generate_file_name(local_file_path: str=None, local_file_bytes: bytes=None):
    if local_file_path == None:
        opened_target_file = local_file_bytes
    else:
        opened_target_file = open(local_file_path, "rb").read()
    md5_part = hashlib.md5(opened_target_file).hexdigest()
    timestamp_part = str(int(datetime.now().timestamp()))
    return timestamp_part+md5_part

def uploadImage(authorization: str, local_file_path: str=None, local_file_bytes: bytes=None, local_file_name: str="", remote_folder_path=""):
    url = "https://api.image4.io/v1.0/uploadImage"
    payload = {"useFilename": "true",
               "overwrite": "true",
               "path": remote_folder_path}
    if local_file_path == None:
        opened_image_file = local_file_bytes
    else:
        opened_image_file = open(local_file_path, "rb")
    files = {"image": (local_file_name, opened_image_file, "application/octet-stream")}
    headers = {
        "Authorization": f"Basic {authorization}"
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.status_code, response.text)
    return response

if __name__ == "__main__":
    TOKEN_FILE = json.load(open("app.token.json"))
    my_auth = calculate_basic_auth(api_key=TOKEN_FILE["image4io"]["api_key"], api_secret=TOKEN_FILE["image4io"]["api_secret"])
    print(my_auth)
    # uploadImage(authorization=my_auth, local_file_path="example.png", local_file_name="example.png")
    print(generate_file_name(local_file_path="example.png"))
    print("finished")