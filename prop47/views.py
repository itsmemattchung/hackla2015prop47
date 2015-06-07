import os
import requests

from django.views.generic.base import TemplateView
from django.shortcuts import render

from .forms import PriorCrimesForm
from .forms import Prop47CrimesForm
from .forms import ResourcesSearchForm


def get_step_view(request, step):
    if int(step) == 1:
        pform = Prop47CrimesForm()
    else:
        pform = PriorCrimesForm()
    return render(
        request,
        template_name="step.html",
        context={"step": step, "form": pform},
    )


class ResourcesSearchView(TemplateView):
    template_name = "resources.html"

    def get_context_data(self, **kwargs):
        context = super(ResourcesSearchView, self).get_context_data(**kwargs)
        form = ResourcesSearchForm(self.request.GET or None)
        context['form'] = form
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']
            url = "https://api.avvo.com/api/1/lawyers/search.json"
            username = os.environ.get('AVVOS_USERNAME')
            password = os.environ.get('AVVOS_APIKEY')
            r = requests.get(url, auth=(username, password), params={
                'loc': zip_code,
                'q': 'Criminal Defense',
            })
            context['search_results'] = r.json()
        return context
