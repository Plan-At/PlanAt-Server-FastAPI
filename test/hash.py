import hashlib

INPUT_TEXT = "abcdefgh"
INPUT_TOKEN = "1234567890"

print(type(hashlib.sha512((INPUT_TOKEN+INPUT_TEXT).encode("utf-8")).hexdigest()))