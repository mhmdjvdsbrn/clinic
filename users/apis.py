from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from .validators import number_validator  ,letter_validator
from .models import BaseUser 
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
# from .selectors import  
from .services import register
from .selectors import get_user
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated


class RegisterApi(APIView):
    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        full_name = serializers.CharField(max_length=35)
        password = serializers.CharField(
                validators=[
                        number_validator,
                        letter_validator,
                        MinLengthValidator(limit_value=10)
                    ]
                )
        confirm_password = serializers.CharField(max_length=255)

        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("email Already Taken")
            return email

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")
            
            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data

    class OutPutRegisterSerializer(serializers.ModelSerializer):
        token = serializers.SerializerMethodField("get_token")
        class Meta:
            model = BaseUser
            fields = ("id", "email" ,"full_name" ,"created","updated" ,"token")
        def get_token(self, user):
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data

    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                email=serializer.validated_data.get("email"),
                full_name=serializer.validated_data.get("full_name"),
                password=serializer.validated_data.get("password"),
                )
        except Exception as ex:
            return Response(
                    f"Database Error {ex}",
                    status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(self.OutPutRegisterSerializer(user, context={"request":request}).data)

class DetaiUser(APIView):
    permission_classes = [IsAuthenticated] 

    class OutPutDetailUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("email" ,"full_name" ,"created","updated")

    @extend_schema(
        responses=OutPutDetailUserSerializer,
    )
    def get(self ,request):
        query = get_user(pk=request.user.pk)
        return Response(self.OutPutDetailUserSerializer(query, context={"request":request}).data)
