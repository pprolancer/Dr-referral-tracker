from django.shortcuts import render
from .forms import OrganizationForm
from .models import Organization
from django.contrib import messages
from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect


class Organization(View):
    # display the Organization form
    def get(self, request, *args, **kwargs):
        form = OrganizationForm()
        ctx = {"form": form}
        return render(request,"tracking/organization.html",ctx )

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST)
        ctx = {"form": form}
        if form.is_valid():
            form.save()
            # messages.warning(request, 'Form have saved successfully....')
        ctx = {"form": form}
        return render(request,"tracking/organization.html",ctx )


class Physician(View):
    # display the physician form
    def get(self, request, *args, **kwargs):
        form = PhysicianForm()
        ctx = {"form": form}
        return render(request,"tracking/organization.html",ctx )

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('', RequestContext(request, {}))
        ctx = {"form": form}
        return render(request, "", ctx)


class Referral(View):
    # display the referral form
    def get(self, request, *args, **kwargs):
        form = ReferralForm()
        ctx = {"form": form}
        return render(request,"tracking/organization.html",ctx )

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('', RequestContext(request, {}))
        ctx = {"form": form}
        return render(request, "", ctx)

