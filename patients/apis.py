from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from .validators import number_validator  ,letter_validator
from .models import Patients 
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
# from .selectors import  
from .services import register, update_patient, delete_patient
from .selectors import patients, detail_Patient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser



class RegisterApi(APIView):
    # permission_classes = [IsAdminUser] 
    class InputRegisterSerializer(serializers.Serializer):
        national_code = serializers.CharField(max_length=10)
        first_name = serializers.CharField(max_length=35)
        last_name = serializers.CharField(max_length=35)
        description = serializers.CharField(max_length=255)
        age = serializers.IntegerField()

        password = serializers.CharField(
                validators=[
                        number_validator,
                        letter_validator,
                        MinLengthValidator(limit_value=10)
                    ]
                )
        confirm_password = serializers.CharField(max_length=255)

        def validate_national_code(self, national_code):
            if Patients.objects.filter(national_code=national_code).exists():
                raise serializers.ValidationError("national_code Already Taken")
            return national_code

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")
            
            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data

    class OutPutRegisterSerializer(serializers.ModelSerializer):
        token = serializers.SerializerMethodField("get_token")
        class Meta:
            model = Patients
            fields = ("id", "national_code" ,"first_name", "last_name", 'age' ,"created","updated" ,"token")
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
                national_code=serializer.validated_data.get("national_code"),
                password=serializer.validated_data.get("password"),
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                age=serializer.validated_data.get("age"),
                description=serializer.validated_data.get("description"),
                )
        except Exception as ex:
            return Response(
                    f"Database Error {ex}",
                    status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(self.OutPutRegisterSerializer(user, context={"request":request}).data)





class GetPatientsApi(APIView):
    permission_classes = [IsAdminUser] 
    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Patients
            fields = ['id','national_code' ,'first_name', 'last_name']

    @extend_schema(
        responses=OutPutSerializer,
    )
    def get(self, request):
        try:
            query = patients()
        except Exception as ex:
            return Response(
                {"detail": "Not Found -- " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.OutPutSerializer(query, many=True)

        return Response(serializer.data) 
    


class DetailPatientsApi(APIView):
    permission_classes = [IsAuthenticated] 
    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Patients
            fields = ['id','national_code', 'first_name', 'last_name', 'age', 'description', 'created',]

    @extend_schema(
        responses=OutPutSerializer,
    )
    def get(self, request):
        try:
            query = detail_Patient(pk=request.user.pk)
        except Exception as ex:
            return Response(
                {"detail": "Not Found -- " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.OutPutSerializer(query)
        return Response(serializer.data) 

    def delete(self, request, pk):
        try:
            delete_patient(pk=request.user.pk)
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)




class UpdatePatientsApi(APIView):
    permission_classes = [IsAuthenticated] 

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Patients
            fields = ['first_name', 'last_name', 'age', 'description',]

    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Patients
            fields = ['id', 'first_name', 'last_name', 'age', 'description', 'created']

    @extend_schema(
        request=InputSerializer,
        responses=OutPutSerializer,
    )
    def put(self, request, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = update_patient(
                pk=pk,
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                age=serializer.validated_data.get("age"),
                description=serializer.validated_data.get("description"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutPutSerializer(query).data)