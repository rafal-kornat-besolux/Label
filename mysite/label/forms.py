from django import forms
from .models import OrderB2C
from django.shortcuts import get_object_or_404

class OrderB2CForm(forms.ModelForm):
    class Meta:
        model = OrderB2C
        fields = '__all__'