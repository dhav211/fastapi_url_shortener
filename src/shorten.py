from random import choices


def create_short_code():
    chars_to_use = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f']
    short_code = choices(chars_to_use, k=8)
    return "".join(short_code)

def strip_url(url: str):
    url = url.removeprefix("https://")
    url = url.removeprefix("http://")
    url = url.removeprefix("www.")
    url = url.removesuffix("/")
    return url