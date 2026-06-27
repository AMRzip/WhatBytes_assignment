from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    def test_user_can_register_and_login_with_email(self):
        register_response = self.client.post(
            reverse("register"),
            {
                "name": "Aarav Sharma",
                "email": "aarav@example.com",
                "password": "strongpass123",
            },
            format="json",
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="aarav@example.com").exists())

        login_response = self.client.post(
            reverse("login"),
            {
                "email": "aarav@example.com",
                "password": "strongpass123",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)
