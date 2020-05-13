from django import forms
from django.core.validators import MaxValueValidator


class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(validators=[MaxValueValidator(1000)])
