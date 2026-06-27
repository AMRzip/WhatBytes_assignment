from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Doctor, Patient


class HealthcareAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="strongpass123",
        )
        self.other_user = User.objects.create_user(
            username="other@example.com",
            email="other@example.com",
            password="strongpass123",
        )
        self.client.force_authenticate(self.user)

    def test_user_can_create_and_list_only_own_patients(self):
        Patient.objects.create(
            user=self.other_user,
            name="Other Patient",
            age=44,
            gender="Female",
            disease="Asthma",
        )

        create_response = self.client.post(
            reverse("patients"),
            {
                "name": "Riya Mehta",
                "age": 29,
                "gender": "Female",
                "disease": "Fever",
            },
            format="json",
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        list_response = self.client.get(reverse("patients"))

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]["name"], "Riya Mehta")

    def test_user_can_manage_doctors_and_patient_mappings(self):
        patient = Patient.objects.create(
            user=self.user,
            name="Kabir Singh",
            age=36,
            gender="Male",
            disease="Diabetes",
        )
        doctor = Doctor.objects.create(
            name="Dr. Naina Rao",
            specialization="Endocrinology",
            experience=8,
        )

        mapping_response = self.client.post(
            reverse("mappings"),
            {
                "patient_id": patient.id,
                "doctor_id": doctor.id,
            },
            format="json",
        )

        self.assertEqual(mapping_response.status_code, status.HTTP_201_CREATED)
        mapping_id = mapping_response.data["mapping"]["id"]

        patient_doctors_response = self.client.get(reverse("mapping_detail", args=[patient.id]))

        self.assertEqual(patient_doctors_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patient_doctors_response.data[0]["name"], "Dr. Naina Rao")

        delete_response = self.client.delete(reverse("mapping_detail", args=[mapping_id]))

        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patient.doctors.count(), 0)

    def test_unauthenticated_requests_are_rejected(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(reverse("patients"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
