from django.contrib import admin
from .models import Volunteer, User, Administrator
# Register your models here.

admin.site.register(User)

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['user','gender', 'birth_date', 'address','city', 'zipcode', 'phone']

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ['user','gender', 'birth_date', 'address','city', 'zipcode', 'phone']


