from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Doctor, Patient
from .serializers import DoctorSerializer, MappingSerializer, PatientSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def patients(request):
    if request.method == "GET":
        patient_records = Patient.objects.filter(user=request.user).prefetch_related("doctors")
        serializer = PatientSerializer(patient_records, many=True)
        return Response(serializer.data)

    serializer = PatientSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def patient_detail(request, pk):
    try:
        patient = Patient.objects.prefetch_related("doctors").get(id=pk, user=request.user)
    except Patient.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = PatientSerializer(patient, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    patient.delete()
    return Response({"message": "Patient deleted successfully"})


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def doctors(request):
    if request.method == "GET":
        doctor_records = Doctor.objects.all()
        serializer = DoctorSerializer(doctor_records, many=True)
        return Response(serializer.data)

    serializer = DoctorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def doctor_detail(request, pk):
    try:
        doctor = Doctor.objects.get(id=pk)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    doctor.delete()
    return Response({"message": "Doctor deleted successfully"})


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def mappings(request):
    through_model = Patient.doctors.through

    if request.method == "GET":
        patient_ids = Patient.objects.filter(user=request.user).values_list("id", flat=True)
        mapping_records = through_model.objects.filter(patient_id__in=patient_ids).select_related(
            "patient",
            "doctor",
        )
        serializer = MappingSerializer(mapping_records, many=True)
        return Response(serializer.data)

    patient_id = request.data.get("patient_id")
    doctor_id = request.data.get("doctor_id")

    if not patient_id or not doctor_id:
        return Response(
            {"error": "patient_id and doctor_id are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        patient = Patient.objects.get(id=patient_id, user=request.user)
        doctor = Doctor.objects.get(id=doctor_id)
    except (Patient.DoesNotExist, Doctor.DoesNotExist, TypeError, ValueError):
        return Response(
            {"error": "Invalid patient or doctor"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if through_model.objects.filter(patient=patient, doctor=doctor).exists():
        return Response(
            {"error": "Doctor is already assigned to this patient"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    patient.doctors.add(doctor)
    mapping = through_model.objects.get(patient=patient, doctor=doctor)
    serializer = MappingSerializer(mapping)

    return Response(
        {
            "message": "Doctor assigned successfully",
            "mapping": serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def mapping_detail(request, pk):
    through_model = Patient.doctors.through

    if request.method == "GET":
        try:
            patient = Patient.objects.prefetch_related("doctors").get(id=pk, user=request.user)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorSerializer(patient.doctors.all(), many=True)
        return Response(serializer.data)

    try:
        mapping = through_model.objects.select_related("patient").get(id=pk)
    except through_model.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)

    if mapping.patient.user != request.user:
        return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)

    mapping.delete()
    return Response({"message": "Doctor removed from patient successfully"})
