from django import forms
from django.contrib.auth.models import User
from .models import Testimonial, SiteUser


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
    account = forms.CharField(max_length=100)
    company = forms.CharField(max_length=100)
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput)

    def save(self, commit=True):
        account = self.cleaned_data['account']
        pin = self.cleaned_data['pin']
        company = self.cleaned_data['company']

        user = User(username=account, password=pin)
        siteuser = SiteUser(company=company)
        siteuser.user = user

        if commit:
            user.save()

        return user


class NewAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class PinResetForm(forms.Form):
    account = forms.CharField(max_length=100)
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput)


class DeleteUserForm(forms.Form):
    account = forms.CharField(max_length=100)


class ListFileForm(forms.Form):
    MODES = (
        ('incoming', 'Filings'),
        ('outgoing', 'Reports'),
    )
    account = forms.CharField(max_length=100)
    mode = forms.ChoiceField(choices=MODES)