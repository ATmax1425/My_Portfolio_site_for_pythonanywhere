import secrets
import string


def get_secret(num=100, simple=False):
    if simple:
        str_ = string.ascii_letters
    else:
        str_ = string.digits + string.punctuation + string.ascii_letters

    secret = "".join(secrets.choice(str_) for _ in range(num))
    return secret


if __name__ == "__main__":
    print(get_secret())
