import random
import string

def generate_password(no_alp=4,no_num=4, no_spl=2):
    password = ''.join(random.choice(string.ascii_letters) for _ in range(no_alp))
    password += ''.join(random.choice(string.digits) for _ in range(no_num))
    password += ''.join(random.choice(string.punctuation) for _ in range(no_spl))
    return password