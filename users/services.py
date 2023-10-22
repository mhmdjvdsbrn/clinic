from django.db.models import QuerySet
from .models import BaseUser 
from django.db import transaction


def create_user(*  ,email:str,full_name:str ,password:str)->BaseUser:
    return BaseUser.objects.create_user(email=email ,full_name=full_name,password=password)

@transaction.atomic
def register(* ,full_name:str ,email:str ,password:str) ->BaseUser:
    user = create_user(email=email,full_name=full_name ,password=password)
    return user