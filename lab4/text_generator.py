import random

def get_rand_lowercase_char():
    return chr(ord('a') + random.randint(0, 25))

def get_random_text(size: int):
    return ''.join((get_rand_lowercase_char() for _ in range(size)))
