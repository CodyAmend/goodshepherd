from django import forms
from .models import Item, Category

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = {'item_name','category', 'description','quantity','available', 'created_date' }
