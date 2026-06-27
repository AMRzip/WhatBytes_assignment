from django.urls import path

from . import views

urlpatterns = [
    path("patients/", views.patients, name="patients"),
    path("patients/<int:pk>/", views.patient_detail, name="patient_detail"),
    path("doctors/", views.doctors, name="doctors"),
    path("doctors/<int:pk>/", views.doctor_detail, name="doctor_detail"),
    path("mappings/", views.mappings, name="mappings"),
    path("mappings/<int:pk>/", views.mapping_detail, name="mapping_detail"),
]
