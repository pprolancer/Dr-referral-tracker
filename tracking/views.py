from .forms import OrganizationForm, ReferralForm, PhysicianForm
from django.views.generic import View
from django.core.urlresolvers import reverse
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
            return redirect(reverse('add-physician'))

        return render(request,"tracking/organization.html",ctx )


class Physician(View):
    # display the physician form
    def get(self, request, *args, **kwargs):
        form = PhysicianForm()
        ctx = {"form": form}
        return render(request,"tracking/physician.html",ctx )

    def post(self, request, *args, **kwargs):
        form = PhysicianForm(request.POST)
        if form.is_valid():
            form.save()
            form = PhysicianForm()

        ctx = {"form": form}
        return render(request,"tracking/physician.html",ctx )


class Referral(View):
    # display the referral form
    def get(self, request, *args, **kwargs):
        form = ReferralForm()
        ctx = {"form": form}
        return render(request,"tracking/referral.html",ctx )

    def post(self, request, *args, **kwargs):
        form = ReferralForm(request.POST)
        if form.is_valid():
            form.save()
        ctx = {"form": form}
        return render(request,"tracking/referral.html",ctx )

