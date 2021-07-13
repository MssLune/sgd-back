import random
import time
from string import ascii_lowercase


def get_random_name(filename: str = None) -> str:
    """
    Return a random name.
    If a filename is given, add the extension.
    """
    ext = ''
    if filename is not None and filename.find('.') > -1:
        ext = '.' + filename.split('.')[-1]
    return (
        ''.join(random.choice(ascii_lowercase + '0123456789')
                for _ in range(16))
        + '_' + str(time.time()).split('.')[-1]
        + '_' + str(time.time()).split('.')[0] + ext
    )
