from django.db.models import QuerySet
from .models import Patients


def patients() -> QuerySet:
    query = Patients.objects.all()
    return query


def detail_Patient(pk) -> Patients:
    query = Patients.objects.get(pk=pk)
    return query