import os
import requests
from django.conf import settings

from django.http import JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

from googleplaces import GooglePlaces
from .forms import ResourcesSearchForm
from .forms import ZipcodeSubmitForm
from .forms import EmailReminderForm
from .forms import FinalFormSubmissionForm


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
    courthouse_results = _get_google_map_search_results(
        term="courthouse",
        zip_code=request.GET.get('zip_code'),
        count=int(request.GET.get('count', 5)))
    return JsonResponse({"courthouses": courthouse_results})


def get_live_scan_results(request):
    livescan_results = _get_google_map_search_results(
        term="Live Scan",
        zip_code=request.GET.get('zip_code'),
        count=int(request.GET.get('count', 5)))
    return JsonResponse({"live_scans": livescan_results})


def get_checklist(request):
    form = ZipcodeSubmitForm()
    if request.method == "POST":
        form = ZipcodeSubmitForm(request.POST)
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']
            return HttpResponseRedirect(reverse("final-checklist", kwargs={"zip_code": zip_code}))
    return render(request, "checklist.html", {"form": form})


def final_checklist(request, zip_code):
    courthouse_results = _get_google_map_search_results("courthouse", zip_code)
    form = FinalFormSubmissionForm(choices=courthouse_results)
    if request.method == "POST":
        return HttpResponseRedirect(reverse("step-1-complete"))
    return render(
        request,
        "final_checklist.html",
        {
            "form": form,
            "zip_code": zip_code
            }
        )


def _get_google_map_search_results(term, zip_code, count=5, radius=20000):
    google_places = GooglePlaces(settings.GOOGLE_MAPS_API_KEY)
    place_results = google_places.nearby_search(
        location=zip_code,
        keyword=term,
        radius=20000,
        types=[]
        )
    map(lambda x: x.get_details(), place_results.places[:count])
    json_results = [{
        "name": tpr.name,
        "address": tpr.formatted_address,
        "website": tpr.website,
        "phone_number": tpr.local_phone_number,
        "url": tpr.url,
        "id": tpr.id,
        "place_id": tpr.place_id
        }
        for tpr in place_results.places[:count]]
    return json_results
