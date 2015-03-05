from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Testimonial, SiteUser


validate_account = RegexValidator(r'^[0-9]{4}\-[0-9]{2}$', message="Account numbers must take the form ####-##")


class LoginForm(forms.Form):
    account = forms.CharField(max_length=7, validators=[validate_account])
    company = forms.CharField(max_length=100)
    password = forms.CharField(max_length=4, widget=forms.PasswordInput)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class TestimonialForm(forms.ModelForm):
    text = forms.CharField(max_length=1000, widget=forms.Textarea)
    postedby = forms.CharField(max_length=1000)
    email = forms.CharField(max_length=100)

    class Meta:
        model = Testimonial
        fields = ('text', 'postedby', 'email')


class NewUserForm(forms.Form):
    account = forms.CharField(max_length=100, validators=[validate_account])
    company = forms.CharField(max_length=100)
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput)

    def save(self):
        account = self.cleaned_data['account']
        pin = self.cleaned_data['pin']
        company = self.cleaned_data['company']

        user = User(username=account)
        user.set_password(pin)
        user.save()
        user.siteuser.company = company
        user.siteuser.save()

        return user


class NewAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class PinResetForm(forms.Form):
    account = forms.CharField(max_length=100, validators=[validate_account])
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput)


class DeleteUserForm(forms.Form):
    account = forms.CharField(max_length=100)


class ListFileForm(forms.Form):
    MODES = (
        ('incoming', 'Filings'),
        ('outgoing', 'Reports'),
    )
    account = forms.CharField(max_length=100, validators=[validate_account])
    mode = forms.ChoiceField(choices=MODES)