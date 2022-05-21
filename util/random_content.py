import random
from datetime import datetime


def get_str_from_base(base: str, length: int) -> str:
    generated_string = ""
    while True:
        generated_string += random.choice(base)
        generated_string = generated_string.replace(" ", "")  # to remove space being generated
        if len(generated_string) == length:
            return generated_string


def get_int(length: int) -> int:
    while True:
        generated_int = int(get_str_from_base(base="1234567890", length=length))
        if len(str(generated_int)) == length:
            return generated_int
        else:
            print("length not match that the result contain space")


def generator_access_token(length: int) -> str:
    return get_str_from_base(base="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", length=length)


def generate_event_id():
    # The event_id is in int
    generated_event_id = int(str(int(datetime.now().timestamp())) + str(get_int(length=6)))
    if len(str(generated_event_id)) != 16:
        raise Exception("random did not generator correct length of number")
    return generated_event_id


def generate_person_id():
    # The person_id is in string
    while True:
        generated_person_id = str(get_int(10))
        return generated_person_id
