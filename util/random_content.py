import random


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
