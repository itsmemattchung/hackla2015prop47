from django import forms
from localflavor.us.forms import USZipCodeField


class FaxFormsForm(forms.Form):
    pass


class ResourcesSearchForm(forms.Form):
    zip_code = USZipCodeField()


class ZipcodeSubmitForm(forms.Form):
    zip_code = USZipCodeField(
        widget=forms.TextInput(attrs={'placeholder': 'zip code'}))


class EmailReminderForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
