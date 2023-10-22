
# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.urls import path ,include
from rest_framework_simplejwt.views import TokenObtainPairView ,TokenRefreshSlidingView ,TokenVerifyView
urlpatterns = [
    path('jwt/' ,include(([

        path('login/' ,TokenObtainPairView.as_view() ,name='login'),
#         path('logout/' ,custom_logout ,name='refresh'),
#         # path('verify/' ,TokenVerifyView.as_view() ,name='verify'),
        ])),name='jwt')
]



