"""prop47 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', TemplateView.as_view(template_name="about.html")),
    url(r'^faq/', TemplateView.as_view(template_name="faq.html")),
    url(r'^legal/', TemplateView.as_view(template_name="legal.html")),
    url(r'^step/(?P<step>[\w-]+)$', views.get_step_view, name="legal-step"),
    url(r'^resources/', views.ResourcesSearchView.as_view()),
    url(r'^resources/$', TemplateView.as_view(template_name="resources.html")),
    url(r'^step3/', views.enter_zip_code),
    url(r'^locations/(?P<zip_code>[\w-]+)$', views.locations_view, name="location-services"),
    url(r'^locations/livescans/$', views.get_live_scan_results, name="live-scan-resources"),
    url(r'^locations/courthouses/$', views.get_court_results, name="court-resources"),
    url(r'^email_reminder/$', views.create_email_reminder, name="email-reminder"),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^complete/1/$', TemplateView.as_view(template_name="step_1_complete.html"), name="step-1-complete"),
    # checklists
    url(r'^checklist/$', views.get_checklist, name="checklist"),
    url(r'^checklist/final$', views.final_checklist, name="final-checklist")
]
