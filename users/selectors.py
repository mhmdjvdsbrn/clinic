from django.db.models import QuerySet
from .models import BaseUser 


def get_user(pk)->BaseUser:
    query = BaseUser.objects.get(pk=pk)
    return query