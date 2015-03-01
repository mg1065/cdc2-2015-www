from django import forms
from .models import Testimonial


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class TestimonialForm(forms.ModelForm):
    text = forms.CharField(max_length=1000, widget=forms.Textarea)
    postedby = forms.CharField(max_length=1000)
    email = forms.CharField(max_length=100)

    class Meta:
        model = Testimonial
