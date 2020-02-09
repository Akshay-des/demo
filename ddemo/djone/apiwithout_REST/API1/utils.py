#from django.utils.decorators import method_decorator
import json

def is_json(user_data):
    try:
        pdata=json.loads(user_data)
        valid=True
    except ValueError:
        valid=False
    return valid

