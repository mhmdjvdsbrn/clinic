from django.db import models
from patients.models import Patients

class Visit(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='patient')
    date_visit = models.DateTimeField(auto_now_add=True)
    medicine_name = models.CharField(max_length=255)
    
# Create your models here.
