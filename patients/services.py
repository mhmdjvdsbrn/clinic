from .models import Patients
from django.db.models import QuerySet
from django.db.models import QuerySet
from django.db import transaction


def create_user(*, national_code:str,password:str, first_name:str,
                 last_name:str, age:int, description:str)->Patients:
    return Patients.objects.create_user(national_code=national_code,password=password, first_name=first_name,
                 last_name=last_name, age=age, description=description)

@transaction.atomic
def register(*, national_code:str,password:str, first_name:str,
                 last_name:str, age:int, description:str) ->Patients:
    user = create_user(national_code=national_code,password=password, first_name=first_name,
                 last_name=last_name, age=age, description=description)
    return user


def update_patient(*, pk, first_name:str, last_name:str, age:int, description:str):
    patient = Patients.objects.get(pk=pk)
    patient.first_name = first_name
    patient.last_name = last_name
    patient.age = age
    patient.description = description
    patient.save()
    return patient


def delete_patient(*, pk)->dict:
    deleted = Patients.objects.get(pk=pk).delete()
    return deleted





