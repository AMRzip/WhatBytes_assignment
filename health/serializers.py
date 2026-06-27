from rest_framework import serializers

from .models import Doctor, Patient


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "name", "specialization", "experience"]


class PatientSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ["id", "user", "name", "age", "gender", "disease", "doctors"]
        read_only_fields = ["user"]


class MappingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    patient = serializers.IntegerField(source="patient_id")
    doctor = serializers.IntegerField(source="doctor_id")
    patient_name = serializers.CharField(source="patient.name")
    doctor_name = serializers.CharField(source="doctor.name")
