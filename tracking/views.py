from .forms import *
from django.views.generic import View, TemplateView, ListView
from django.views.generic.edit import FormView

import calendar
from django.db.models import Sum,Count
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime , timedelta, date
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from tracking.models import Referral,Physician, Organization, LAST_MONTH, LAST_12_MONTH
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from tracking.templatetags.visite_counts import get_organization_counts, \
    get_organization_counts_month_lastyear, get_organization_counts_year, \
    get_organization_counts_year_lastyear
from Practice_Referral.settings import TIME_ZONE


class IndexView(View):
    # display the Organization form
    # template_name = "index.html"
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        orgform = OrganizationForm()
        phyform = PhysicianForm()
        refform = ReferralForm()

        today_date = datetime.now().date()
        start_date = today_date - timedelta(days=365)
        end_date = today_date - timedelta(days=1)

        physician_visit_sum = Physician.objects.filter(
            Referral__visit_date__range=(start_date,end_date)).annotate(
            total_visits=Sum('Referral__visit_count')
            ).order_by('-total_visits')[:10]

        org_visit_sum =  Organization.objects.filter(
            Physician__Referral__visit_date__range=(start_date,end_date)).annotate(
            total_org_visits=Sum('Physician__Referral__visit_count')
            ).order_by('-total_org_visits')[:5]

        special_visit_sum =  Organization.objects.filter(org_special=True).filter(
            Physician__Referral__visit_date__range=(start_date,end_date)).annotate(
            total_org_special_visits=Sum('Physician__Referral__visit_count')
            ).order_by('-total_org_special_visits')[:5]

        referrals = Referral.objects.filter(visit_date__range=[LAST_12_MONTH,LAST_MONTH])

        if referrals:
            try:
                referrals = referrals.extra(select={'month': 'STRFTIME("%m",visit_date)'})
                print (referrals[0].month)
            except:
                referrals = referrals.extra(select={'month': 'EXTRACT(month FROM visit_date)'})
            referrals = referrals.values('month').annotate(total_visit_count=Sum('visit_count'))

            for referral in referrals:
                if LAST_MONTH.month <= int(referral['month']) :
                    current_month = date(day=LAST_MONTH.day, month= int(referral['month']), year=LAST_MONTH.year)
                else:
                    current_month = date(day=LAST_12_MONTH.day, month= int(
                        referral['month']), year=LAST_12_MONTH.year)

                last_month = current_month-timedelta(days=364)
                referrals_year = Referral.objects.filter(
                    visit_date__range=[last_month, current_month]).aggregate(year_total=Sum('visit_count'))
                referral['year_total'] = referrals_year['year_total']
                referral['year_from'] = last_month
                referral['year_to'] = current_month
        today = date.today()
        week_ago = today - timedelta(days=7)
        all_orgs = Physician.objects.order_by('physician_name')
        all_ref = {}
        for phys in all_orgs :
            phys_ref = phys.get_referral({'from_date' : week_ago, 'to_date' : today});
            if phys_ref.count() :
                for ref in phys_ref :
                    if not phys.id in all_ref :
                        all_ref[phys.id] = {'name' : phys.physician_name, 'refs' :  [ ref ] }
                    else :
                        all_ref[phys.id]['refs'].append(ref)

        ctx = {
            "orgform": orgform,
            "phyform": phyform,
            "refform": refform,
            "physician_visit_sum": physician_visit_sum,
            "org_visit_sum": org_visit_sum,
            "special_visit_sum": special_visit_sum,
            "referrals":referrals,
            "all_orgs" : all_ref,
            'today': today,
            'week_ago' : week_ago,
            'timezone': TIME_ZONE,
            }
        return render(request,"index.html",ctx )

    def post(self, request, *args, **kwargs):

        phyform = PhysicianForm()
        orgform = OrganizationForm()
        refform = ReferralForm()

        if 'phyform' in request.POST:
            phyform = PhysicianForm(request.POST)
            if phyform.is_valid():
                phyform.save()
                return redirect(reverse('index'))

        elif 'orgform' in request.POST:
            orgform = OrganizationForm(request.POST)
            if orgform.is_valid():
                orgform.save()
                return redirect(reverse('index'))

        elif 'refform' in request.POST:
            refform = ReferralForm(request.POST)
            if refform.is_valid():
                refform.save()
                return redirect(reverse('index'))

        ctx = {
            "orgform": orgform,
            "phyform": phyform,
            "refform": refform,
            'timezone': TIME_ZONE,
          }

        return render(request,"index.html",ctx )

class OrganizationView(View):
    # display the Organization form
    @method_decorator(login_required)
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


class PhysicianView(View):
    # display the physician form
    @method_decorator(login_required)
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


class ReferralView(View):
    # display the referral form
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = ReferralForm()
        ctx = {"form": form, 'timezone': TIME_ZONE}
        return render(request,"tracking/referral.html",ctx )

    def post(self, request, *args, **kwargs):
        form = ReferralForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add/referral/')
        ctx = {"form": form, 'timezone': TIME_ZONE}
        return render(request,"tracking/referral.html",ctx )

class GetReferralReport(View):
    """
    Display a summary of referrals by Organization:provider:
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        all_orgs = Organization.objects.all().order_by('org_name')
        today = datetime.now().date()
        last_year = today.year - 1
        orgs_counts = {}
        total_counts = dict(counts=0, counts_month_lastyear=0,
                            counts_year=0, counts_year_lastyear=0)
        for org in all_orgs:
            counts = get_organization_counts(org)
            counts_month_lastyear = get_organization_counts_month_lastyear(org)
            counts_year = get_organization_counts_year(org)
            counts_year_lastyear = get_organization_counts_year_lastyear(org)
            orgs_counts[org.id] = dict(
                counts=counts,
                counts_month_lastyear=counts_month_lastyear,
                counts_year=counts_year,
                counts_year_lastyear=counts_year_lastyear,
            )
            total_counts['counts'] += counts
            total_counts['counts_month_lastyear'] += counts_month_lastyear
            total_counts['counts_year'] += counts_year
            total_counts['counts_year_lastyear'] += counts_year_lastyear

        ctx = {
                'all_orgs': all_orgs,
                'last_year': last_year,
                'orgs_counts': orgs_counts,
                'total_counts': total_counts
            }
        return render(request, "tracking/show_referral_report.html", ctx)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('/')

class GetReferralHistory(View):
    """
    Display a summary of referrals by Date:Physician:Organization:Count:
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        today = date.today()
        referrals = Referral.objects.filter(visit_date=today).order_by('-visit_date')
        form = ReferralHistoryForm(initial={'from_date': today, 'to_date' : today})
        ctx = {
                'referrals': referrals,
                'timezone': TIME_ZONE,
                "form": form
            }
        return render(request,"tracking/show_referral_history.html",ctx )


    def post(self, request, *args, **kwargs):

        form = ReferralHistoryForm(request.POST)
        if form.is_valid():
            cleaned_data = form.clean()
            referrals = Referral.objects\
                .filter(visit_date__gte=cleaned_data['from_date'])\
                .filter(visit_date__lte=cleaned_data['to_date'])\
                .order_by('-visit_date')
            if cleaned_data['physician']:
                referrals = referrals.filter(physician__in=cleaned_data['physician'])
        else:
            referrals = []

        ctx = {
            'referrals': referrals,
            'timezone': TIME_ZONE,
            "form": form
        }
        return render(request,"tracking/show_referral_history.html",ctx )

def edit_physician(request, physician_id):
    physician = get_object_or_404(Physician, id=physician_id)
    if request.method == 'POST':
        form = PhysicianForm(request.POST, instance=physician)
        if form.is_valid():
            form.save()
            return render(request, 'tracking/physician_edit.html', {
                'form': form,
                'success': True})

    else:
        form = PhysicianForm(instance=physician)

    return render(request, 'tracking/physician_edit.html', {'form': form})

def edit_organization(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return render(request, 'tracking/organization_edit.html', {
                'form': form,
                'success': True})

    else:
        form = OrganizationForm(instance=organization)

    return render(request, 'tracking/organization_edit.html', {'form': form})

class OrganizationView(ListView):
    model = Organization
    template_name = 'tracking/organization_list.html'
    context_object_name = "organizations"
    paginate_by = 10

class PhysicianView(ListView):
    model = Physician
    template_name = 'tracking/physician_list.html'
    context_object_name = "physicians"
    paginate_by = 10
