from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

GENDER = (
    ('M', 'Male'),
    ('F', 'Female')
)

class User(AbstractUser):
    is_administrator = models.BooleanField(default=False)
    is_volunteer = models.BooleanField(default=False)

class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=10, verbose_name="Gender", choices=GENDER)
    birth_date = models.DateField(verbose_name="Birth date", default="1900-01-01")
    address = models.CharField(max_length=100, verbose_name="Mailing Address")
    city = models.CharField(max_length=50, verbose_name="City")
    zipcode = models.CharField(max_length=20, verbose_name="Zipcode")
    phone = models.CharField(max_length=10, verbose_name="Phone number")
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=10,verbose_name="Gender", choices=GENDER)
    birth_date = models.DateField(verbose_name="Birth date", default="1900-01-01")
    address = models.CharField(max_length=100,verbose_name="Mailing Address")
    city = models.CharField(max_length=50, verbose_name="City")
    zipcode = models.CharField(max_length=20, verbose_name="Zipcode")
    phone = models.CharField(max_length=10,verbose_name="Phone number")
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()