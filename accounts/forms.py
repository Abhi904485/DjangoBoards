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
        'password_mismatch': _('The two password fields did’t match.'),
    }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': self.fields['username'].label})
        self.fields['email'].widget.attrs.update({'placeholder': self.fields['email'].label})
        self.fields['first_name'].widget.attrs.update({'placeholder': self.fields['first_name'].label})
        self.fields['last_name'].widget.attrs.update({'placeholder': self.fields['last_name'].label})
        self.fields['password1'].widget.attrs.update({'placeholder': "Enter password"})
        self.fields['password2'].help_text = "<li>Password should be 8 characters in length</li><li>Password should Contain special Characters</li>"
        self.fields['password2'].widget.attrs.update({'placeholder': "Confirm password"})

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

    def add_error(self, field, error):
        return super().add_error(field, error)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password1', error=self.error_messages['password_mismatch'])
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


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'readonly': 'true'})


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
                                widget=forms.PasswordInput({'autocomplete': 'new-password'}), required=True,
                                error_messages={'required': 'Please Enter new Password'})
    password2 = forms.CharField(label="Confirm Password", max_length=128, strip=False,
                                widget=forms.PasswordInput({'autocomplete': 'new-password'}), required=True,
                                error_messages={'required': 'Please Re Enter New Password'})

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password1', error=self.error_messages['password_mismatch'])
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def add_error(self, field, error):
        return super().add_error(field, error)


class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(validators=[MaxValueValidator(500)])


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(label="Old Password", max_length=128, strip=False,
                                widget=forms.PasswordInput({'autocomplete': 'new-password'}), required=True,
                                error_messages={'required': "Please Enter The Existing Password"})
    password2 = forms.CharField(label="New Password", max_length=128, strip=False,
                                widget=forms.PasswordInput({'autocomplete': 'new-password'}), required=True,
                                error_messages={"required": "Please Enter The New Password "})

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and not password2:
            self.add_error('password1', error="Please Enter The Existing Password")
        if not password1 and password2:
            self.add_error('password2', "Please Enter The New Password")
        return cleaned_data

    def add_error(self, field, error):
        return super().add_error(field, error)
