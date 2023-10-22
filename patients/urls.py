from django.urls import path
from .apis import RegisterApi, GetPatientsApi, DetailPatientsApi, UpdatePatientsApi
urlpatterns = [
    path('new-patient/', RegisterApi.as_view()),

    path('update-patient/<int:pk>/', UpdatePatientsApi.as_view()),

    path('', GetPatientsApi.as_view()),
    path('detail-patient/', DetailPatientsApi.as_view()),



]