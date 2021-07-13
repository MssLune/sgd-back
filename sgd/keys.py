
from django.conf import settings

with open(settings.BASE_DIR / 'keys' / 'private.pem', 'r') as content_file:
    private_key = content_file.read()

with open(settings.BASE_DIR / 'keys' / 'public.pem', 'r') as content_file:
    public_key = content_file.read()

JWT_PRIVATE_KEY = private_key
JWT_PUBLIC_KEY = public_key
