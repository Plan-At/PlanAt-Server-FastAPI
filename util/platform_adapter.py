import sys
import requests


def get_mongodb_session():
    if sys.platform == "win32":
        return requests.Session()
