from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.conf import settings


class User(AbstractUser):

    ROLE_CHOICES = (
        ("COMMUTER", "Commuter"),
        ("VALIDATOR", "Validator"),
        ("ADMIN", "Admin"),
    )

    mobile = models.CharField(max_length=15)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class TransportMode(models.Model):

    name = models.CharField(max_length=50)

    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class PassType(models.Model):

    name = models.CharField(max_length=50)

    validity_days = models.IntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    transport_modes = models.ManyToManyField(TransportMode)

    max_trips_per_day = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserPass(models.Model):

    STATUS_CHOICES = (("ACTIVE", "Active"), ("EXPIRED", "Expired"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    pass_type = models.ForeignKey(PassType, on_delete=models.CASCADE)

    pass_code = models.CharField(max_length=100, unique=True)

    purchase_date = models.DateTimeField(auto_now_add=True)

    expiry_date = models.DateTimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.pass_code


class Trip(models.Model):

    user_pass = models.ForeignKey(UserPass, on_delete=models.CASCADE)

    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    transport_mode = models.ForeignKey(TransportMode, on_delete=models.CASCADE)

    route_info = models.CharField(max_length=200, null=True, blank=True)

    validated_at = models.DateTimeField(auto_now_add=True)
