import random

def get_str_from_base(base: str, length: int):
    return ("".join(random.choice(base) for i in range(length)))

def get_int(length: int):
    return int(get_str_from_base(base="1234567890", length=length))
