from django import forms
from localflavor.us.forms import USZipCodeField


class FaxFormsForm(forms.Form):
    pass

class StayUpdatedForm(forms.Form):
    name = forms.CharField(label='Your name')
    email_address = forms.EmailField()

class ResourcesSearchForm(forms.Form):
    zip_code = USZipCodeField(
        widget=forms.TextInput(attrs={'placeholder': 'zip code'}))


class ZipcodeSubmitForm(forms.Form):
    zip_code = USZipCodeField(
        widget=forms.TextInput(attrs={'placeholder': 'zip code'}))


class EmailReminderForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'name'}))
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'email'}))


class FinalFormSubmissionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    # file fields
    criminal_records = forms.FileField()
    live_scan_docs = forms.FileField()
    reclassification = forms.FileField()

    def __init__(self, choices, *args, **kwargs):
        super(FinalFormSubmissionForm, self).__init__(*args, **kwargs)
        choices = [(item["id"], item["name"]) for item in choices]
        self.fields['choices'] = forms.ChoiceField(choices=choices)
