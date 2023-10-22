from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .models import Visit
from patients.models import Patients

from .services import create_visit, delete_visit ,update_visit
from .selectors import visits, detail_visit, detail_visit_patient
from patients.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
class PatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = ['id', 'last_name']

class CreateVisitApi(APIView):
    permission_classes = [IsAdminUser] 
    class InputSerializerVisit(serializers.ModelSerializer):

        class Meta:
            model = Visit
            fields = ['patient', 'medicine_name']


    class OutPutSerializerVisit(serializers.ModelSerializer):
        patient = PatientsSerializer()
        class Meta:
            model = Visit
            fields = ['id', 'patient', 'medicine_name', 'date_visit']

    @extend_schema(
        responses=OutPutSerializerVisit,
        request=InputSerializerVisit,
    )
    def post(self, request):
        serializer = self.InputSerializerVisit(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = create_visit(
                patient=serializer.validated_data.get("patient"),
                medicine_name=serializer.validated_data.get("medicine_name"),

            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutPutSerializerVisit(query, context={"request":request}).data)

class GetVisitsApi(APIView):
    permission_classes = [IsAdminUser] 

    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Visit
            fields = ['id', 'patient', 'medicine_name', 'date_visit']

    @extend_schema(
        responses=OutPutSerializer,
    )
    def get(self, request):

        try:
            query = visits()
        except Exception as ex:
            return Response(
                {"detail": "Not Found -- " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.OutPutSerializer(query, many=True)

        return Response(serializer.data) 
    


class DetailVisitApi(APIView):
    permission_classes = [IsAdminUser] 

    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Visit
            fields = ['id', 'patient', 'medicine_name', 'date_visit']

    @extend_schema(
        responses=OutPutSerializer,
    )
    def get(self, request, pk):
        try:
            query = detail_visit(pk=pk)
        except Exception as ex:
            return Response(
                {"detail": "Not Found -- " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.OutPutSerializer(query)
        return Response(serializer.data) 

    def delete(self, request, pk):
        try:
            delete_visit(pk=pk)
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateVisitsApi(APIView):

    class InputSerializerVisit(serializers.ModelSerializer):
        class Meta:
            model = Visit
            fields = ['patient', 'medicine_name']
    class OutPutSerializerVisit(serializers.ModelSerializer):
        patient = PatientsSerializer()
        class Meta:
            model = Visit
            fields = ['id', 'patient', 'medicine_name', 'date_visit']


    @extend_schema(
        request=InputSerializerVisit,
        responses=OutPutSerializerVisit,
    )
    def put(self, request, pk):
        permission_classes = (IsAdminUser,)
        serializer = self.InputSerializerVisit(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = update_visit(
                pk=pk,
                patient=serializer.validated_data.get("patient"),
                medicine_name=serializer.validated_data.get("medicine_name"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutPutSerializerVisit(query).data)





class DetailVisitPatientApi(APIView):
    permission_classes = [IsAuthenticated] 
    class OutPutSerializer(serializers.ModelSerializer):
        patient= PatientsSerializer()
        class Meta:
            model = Visit
            fields = ['id', 'patient', 'medicine_name', 'date_visit']

    @extend_schema(
        responses=OutPutSerializer,
    )
    def get(self, request):
        try:
            query = detail_visit_patient(patient=request.user)
        except Exception as ex:
            return Response(
                {"detail": "Not Found -- " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.OutPutSerializer(query, many=True)
        return Response(serializer.data) 
