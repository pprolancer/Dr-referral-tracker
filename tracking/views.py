from django.shortcuts import render
from .forms import OrganizationForm
from django.contrib import messages
from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect

# class ReferralReport(ListView):
#     """
#     See Referral Report.pdf in misc folder for example of this view
#     """

class organization(View):
    # display the Organization form
    def get(self, request, *args, **kwargs):
        form = OrganizationForm()
        ctx = {"form": form}
        return render(request,"tracking/welcome.html",ctx )

    def post(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        form = OrganizationForm(request.POST)
        ctx = {"form": form}
        if form.is_valid():

            form.save()
            # messages.warning(request, 'Form have saved successfully....')
        form = OrganizationForm()
        ctx = {"form": form}
        return render(request,"tracking/welcome.html",ctx )

class physician(View):
    # display the physician form
    def get(self, request, *args, **kwargs):
        form = PhysicianForm()
        ctx = {"form": form}
        return render(request,"tracking/welcome.html",ctx )

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('', RequestContext(request, {}))
        ctx = {"form": form}
        return render(request, "", ctx)


class referral(View):
    # display the referral form
    def get(self, request, *args, **kwargs):
        form = ReferralForm()
        ctx = {"form": form}
        return render(request,"tracking/welcome.html",ctx )

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('', RequestContext(request, {}))
        ctx = {"form": form}
        return render(request, "", ctx)

