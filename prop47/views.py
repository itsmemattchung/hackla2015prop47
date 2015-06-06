from django.views.generic.base import TemplateView
from django.shortcuts import render

from .forms import PriorCrimesForm
from .forms import Prop47CrimesForm

def get_step_view(request, step):
    if int(step) == 1:
        pform = Prop47CrimesForm()
    else:
        pform = PriorCrimesForm()
    return render(
        request,
        template_name="step.html",
        context={"step":step, "form":pform},
        )
