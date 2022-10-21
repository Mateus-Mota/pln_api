from slugify import slugify


def username_slugify(username: str):
    """
    ....
    """
    return slugify(username, lowercase=False)
