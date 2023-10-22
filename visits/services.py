from patients.models import Patients
from .models import Visit
from django.db.models import QuerySet

def create_visit(*, patient:str, medicine_name:str) -> dict:
    visit = Visit.objects.create(
        patient=patient, medicine_name=medicine_name
    )
    return visit
    
def update_visit(*, pk, patient:int, medicine_name:str,):
    visit = Visit.objects.get(pk=pk)
    visit.patient = patient
    visit.medicine_name = medicine_name
    visit.save()
    return visit

def delete_visit(*, pk) -> dict:
    deleted = Visit.objects.get(pk=pk).delete()
    return deleted


