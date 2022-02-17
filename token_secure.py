import hashlib

INPUT_TEXT = "abcdefgh"
INPUT_TOKEN = "1234567890"

print(hashlib.sha512((INPUT_TEXT+INPUT_TOKEN).encode("utf-8")).hexdigest())