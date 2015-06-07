from django import forms
from localflavor.us.forms import USZipCodeField


PROP_47_CRIMES = (
    ("HD", "Haberdashery"),
    ("ST", "Sartorialisation"),
    ("PH", "Poor Hygene"),
    )

PRIOR_CRIMES = (
    ("BL", "Blarney"),
    ("SK", "Skullduggery"),
    ("TF", "Tomfoolery"),
    )


class PriorCrimesForm(forms.Form):
    prior_crimes = forms.MultipleChoiceField(
        choices=PRIOR_CRIMES,
        required=False,
        widget=forms.SelectMultiple
        )


class Prop47CrimesForm(forms.Form):
    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple,
        choices=PROP_47_CRIMES
        )


class FaxFormsForm(forms.Form):
    pass


class ResourcesSearchForm(forms.Form):
    zip_code = USZipCodeField()
