import random
import string

from models import *

def generate_random_tag():
    tag_exists = True
    while tag_exists:
        random_tag = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        tag_exists = check_tag_exists(random_tag)
    return random_tag

def check_tag_exists(tag):
    worker = Worker.get_or_none(tag=tag)
    return bool(worker)

