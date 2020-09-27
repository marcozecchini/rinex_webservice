from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, RinexMetadata, license_list

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class UploadFileForm(forms.Form):
    file = forms.FileField()
    licence = forms.MultipleChoiceField(
       # widget=forms.SelectMultiple,
        choices=license_list,
    )
    
class SearchFileForm(forms.Form):
    min_lon = forms.FloatField(required=False, label="Minimum longitude")
    min_lat = forms.FloatField(required=False, label="Minimum latitude")
    max_lon = forms.FloatField(required=False, label="Maximum longitude")
    max_lat = forms.FloatField(required=False, label="Maximum latitude")

    receiver_info = forms.CharField(required=False, label="Receiver Information")
    antenna_info = forms.CharField(required=False, label="Antenna Information")

    start_time = forms.DateTimeField(required=False)
    finish_time = forms.DateTimeField(required=False)

    system_info = forms.CharField(required=False, label="Systems")
    number_sys_info = forms.IntegerField(required=False, label="Number of systems")
    dual_frequency = forms.CheckboxInput()

    #TODO per la licenza multiple choice field

    # upload_time = forms.