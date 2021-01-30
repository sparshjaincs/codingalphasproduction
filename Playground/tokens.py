from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
import pickle
from itsdangerous import URLSafeSerializer


def verify_secret_key(token):
    s = URLSafeSerializer("secret-key")
    return s.loads(token)


def get_secret_key(token_obj):
    s = URLSafeSerializer("secret-key")
    s = s.dumps(token_obj)
    return s
 

