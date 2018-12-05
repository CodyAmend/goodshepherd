from django import forms
from .models import Customer, Visit, VisitItems
from django.forms import inlineformset_factory
from django.contrib import messages
import django_filters

YEARS = [x for x in range(1940, 2019)]

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'gender', 'birth_date', 'address','city', 'zipcode', 'phone','is_employed', 'employer',
                  'family_size','items_needed')

        widgets = {
            #'birth_date': forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'})
            'birth_date': forms.SelectDateWidget(years=YEARS)
        }


        # grabbing the relevant fields in our form, and setting the initial values
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['employer'].required = False
        self.fields['is_employed'].required = False
        self.fields['is_employed'].initial = False
        #self.fields['employer'].widget.attrs['disabled'] = 'True'



    # If is_employed is checked than Employer should be present.
    def clean(self):
        is_employed = self.cleaned_data.get("is_employed")
        employer = self.cleaned_data.get("employer")
        if is_employed:
            if employer == "":
                #self.fields['employer'].widget.attrs['disabled'] = 'False'
                raise forms.ValidationError("Employer is a required field.")
            if employer == "NO" or employer == "no" or employer == "No":
                raise forms.ValidationError("Please enter valid Employer.")
            if employer == "NONE" or employer == "none" or employer == "None":
                raise forms.ValidationError("Please enter valid Employer.")
            if employer == "-":
                raise forms.ValidationError("Please enter valid Employer.")
        elif is_employed is False and employer != "":
            self.cleaned_data['is_employed'] = True
        return self.cleaned_data

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = [ 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(ClientFilter, self).__init__(*args, **kwargs)
        # at sturtup user doen't click Submit button, and QueryDict (in data) is empty
        if self.data == {}:
            self.queryset = self.queryset.none()

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['client','picked_up']

class VisitItemInline(forms.ModelForm):
        model = VisitItems
        fields = ['item','quantity']

