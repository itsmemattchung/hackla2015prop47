from django import forms


class PriorCrimesForm(forms.Form):
    PRIOR_CRIMES = (
        ("BL", "Blarney"),
        ("SK", "Skullduggery"),
        ("TF", "Tomfoolery"),
        )
    prior_crimes = forms.ChoiceField(choices=PRIOR_CRIMES)


class Prop47CrimesForm(forms.Form):
    PRIOR_CRIMES = (
        ("HD", "Haberdashery"),
        ("ST", "Sartorialisation"),
        ("PH", "Poor Hygene"),
        )
    prop47_crimes = forms.ChoiceField(choices=PRIOR_CRIMES)


class FaxFormsForm(forms.Form):
    pass

