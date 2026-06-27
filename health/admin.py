from django.contrib import admin

from .models import Doctor, Patient


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "specialization", "experience")
    search_fields = ("name", "specialization")
    list_filter = ("specialization",)
    ordering = ("name",)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "gender", "disease", "user")
    search_fields = ("name", "disease", "user__username", "user__email")
    list_filter = ("gender", "disease")
    filter_horizontal = ("doctors",)
    ordering = ("name",)
