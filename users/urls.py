from django.urls import path
from .apis import RegisterApi  ,DetaiUser

urlpatterns = [

    path('register/', RegisterApi.as_view(),name="register"),
    path('detail/', DetaiUser.as_view(),name="user"),
]