import random 
import string

chars = string.ascii_letters + string.digits
def generate_hash():
    return ''.join(random.choices(chars, k=12))