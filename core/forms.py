from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  Administrator, Volunteer, User

YEARS = [x for x in range(1900, 2019)]

class AdministratorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_administrator = True
        if commit:
            user.save()
        return user

class VolunteerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_volunteer = True
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ('gender', 'birth_date', 'address','city', 'zipcode', 'phone')

        widgets = {
            'birth_date': forms.SelectDateWidget(years=YEARS)
        }

class AdministratorForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ('gender', 'birth_date', 'address','city', 'zipcode', 'phone')

        widgets = {
            'birth_date': forms.SelectDateWidget(years=YEARS)
        }
