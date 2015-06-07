from django import forms
from localflavor.us.forms import USZipCodeField

class FaxFormsForm(forms.Form):
    pass


class ResourcesSearchForm(forms.Form):
    zip_code = USZipCodeField()
