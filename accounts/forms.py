from django import forms
from django.contrib.auth import password_validation
from django.core.validators import MaxValueValidator, validate_email

from .models import User
from django.utils.translation import ugettext_lazy as _


# from django.contrib.auth.forms import  UserCreationForm

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", max_length=128, strip=False,
                                widget=forms.PasswordInput({'autocomplete': 'new-password'}))
    password2 = forms.CharField(label="Confirm Password", max_length=128, strip=False,
                                widget=forms.PasswordInput({'autocomplete': 'new-password'}))

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=254, strip=True, widget=forms.EmailInput(),
                            help_text=" Enter a Valid Email", error_messages={'required': 'Email is Required'})
    password = forms.CharField(label="Password", max_length=128, strip=False, widget=forms.PasswordInput(),
                               help_text="Enter a valid password", error_messages={'required': 'Password is Required'})

    # class Meta:
    #     model = User
    #     fields = ['email', 'password']


class PasswordResetForm(forms.Form):
    email = forms.CharField(label="Email", max_length=254, strip=True, widget=forms.EmailInput(), required=True,
                            error_messages={'required': 'Please Enter your Email'}, validators=[validate_email])


class PasswordResetConfirm(forms.Form):
    password1 = forms.CharField(label="Password", max_length=128, strip=False,
                                widget=forms.PasswordInput({'autocomplete': 'new-password'}), required=True)
    password2 = forms.CharField(label="Confirm Password", max_length=128, strip=False,
                                widget=forms.PasswordInput({'autocomplete': 'new-password'}), required=True)

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(validators=[MaxValueValidator(500)])


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(label="Password", max_length=128, strip=False,
                                widget=forms.PasswordInput({'autocomplete': 'new-password'}), required=True,
                                error_messages={'required': "Please Enter old password"})
    password2 = forms.CharField(label="Confirm Password", max_length=128, strip=False,
                                widget=forms.PasswordInput({'autocomplete': 'new-password'}), required=True,
                                error_messages={"required": "Enter the new password "})
