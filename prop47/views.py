import os
import requests
from django.conf import settings

from django.http import JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from googleplaces import GooglePlaces
from .forms import ResourcesSearchForm
from .forms import ZipcodeSubmitForm
from .forms import EmailReminderForm


def get_step_view(request, step):
    form = ResourcesSearchForm(request.GET or None)
    return render(
        request,
        template_name="step.html",
        context={"step": step, "form": form}
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


def create_email_reminder(request):
    if request.method == "POST":
        form = EmailReminderForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("step-1-complete"))
    return JsonResponse({"message": "Your reminder has been created!", "success": True})


def print_result_instructions(request):
    return JsonResponse({"message": "Here are your instructions!", "success": True})


def enter_zip_code(request):
    form = ZipcodeSubmitForm(request.GET or None)
    if request.method == "POST":
        form = ZipcodeSubmitForm(request.POST)
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']
            return HttpResponseRedirect(reverse("location-services", kwargs={"zip_code": zip_code}))
    return render(request, "enterzip.html", {"form": form})


def locations_view(request, zip_code):
    form = EmailReminderForm()
    return render(
        request,
        "location_services.html",
        {"zip_code": zip_code, "form": form})


def get_court_results(request):
    google_places = GooglePlaces(settings.GOOGLE_MAPS_API_KEY)
    results_count = int(request.GET.get('count', 5))
    place_results = google_places.nearby_search(
        location=request.GET.get('zip_code'),
        keyword="Courthouse",
        radius=20000,
        types=[]
        )
    map(lambda x: x.get_details(), place_results.places[:results_count])
    json_results = [{
        "name": tpr.name,
        "address": tpr.formatted_address,
        "website": tpr.website,
        "phone_number": tpr.local_phone_number,
        "url": tpr.url
        }
        for tpr in place_results.places[:results_count]]
    return JsonResponse({"courthouses": json_results})


def get_live_scan_results(request):
    google_places = GooglePlaces(settings.GOOGLE_MAPS_API_KEY)
    results_count = request.GET.get('count', 5)
    place_results = google_places.nearby_search(
        location=request.GET.get('zip_code'),
        keyword="Live Scan",
        radius=20000,
        types=[]
        )
    map(lambda x: x.get_details(), place_results.places[:results_count])
    json_results = [{
        "name": tpr.name,
        "address": tpr.formatted_address,
        "website": tpr.website,
        "phone_number": tpr.local_phone_number,
        "url": tpr.url
        }
        for tpr in place_results.places[:results_count]]
    return JsonResponse({"live_scans": json_results})


def get_checklist(request):
    form = ZipcodeSubmitForm()
    return render(request, "checklist.html", {"form": form})


def final_checklist(request):
    return render(request, "final_checklist.html", {})
