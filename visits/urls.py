from django.urls import path
from .apis import CreateVisitApi, GetVisitsApi, DetailVisitApi, UpdateVisitsApi, DetailVisitPatientApi

urlpatterns = [
    path('new-visit/', CreateVisitApi.as_view()),

    path('update-visit/<int:pk>/', UpdateVisitsApi.as_view()),

    path('', GetVisitsApi.as_view()),
    path('<int:pk>/', DetailVisitApi.as_view()),

    path('me/', DetailVisitPatientApi.as_view()),


]