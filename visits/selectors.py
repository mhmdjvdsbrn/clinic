from django.db.models import QuerySet
from .models import Visit


def visits() -> QuerySet:
    query = Visit.objects.all()
    return query

def detail_visit(pk) -> Visit:
    query = Visit.objects.get(pk=pk)
    return query

def detail_visit_patient(patient):
    query = Visit.objects.filter(patient=patient)
    return query
