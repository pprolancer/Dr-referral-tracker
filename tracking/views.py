from .forms import *
from django.views.generic import View, TemplateView, ListView
from django.views.generic.edit import FormView
from django.contrib import messages

import calendar
from django.db.models import Sum,Count
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime , timedelta, date
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from tracking.models import PatientVisit,ReferringEntity, Organization, LAST_MONTH, LAST_12_MONTH
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from tracking.templatetags.visite_counts import get_organization_counts, \
    get_organization_counts_month_lastyear, get_organization_counts_year, \
    get_organization_counts_year_lastyear
from Practice_Referral.settings import TIME_ZONE


class LoginRequiredMixin(object):
    '''
    a Mixin class to check login in class views. View calsses can inherit
    from this class to enforce login_required.
    '''
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        '''
        check login_required for every actions(get, post, ...) by
        this dispatcher
        '''
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class IndexView(LoginRequiredMixin, View):
    # display the Organization form
    # template_name = "index.html"
    @staticmethod
    def get_context(initial_ctx=None):
        '''create context structure for both get and post handlers'''

        orgform = OrganizationForm()
        phyform = ReferringEntityForm()
        refform = PatientVisitForm()

        today_date = datetime.now().date()
        start_date = today_date - timedelta(days=365)
        end_date = today_date - timedelta(days=1)

        referring_entity_visit_sum = ReferringEntity.objects.filter(
            PatientVisit__visit_date__range=(start_date,end_date)).annotate(
            total_visits=Sum('PatientVisit__visit_count')
            ).order_by('-total_visits')[:10]

        org_visit_sum =  Organization.objects.filter(
            ReferringEntity__PatientVisit__visit_date__range=(start_date,end_date)).annotate(
            total_org_visits=Sum('ReferringEntity__PatientVisit__visit_count')
            ).order_by('-total_org_visits')[:5]

        special_visit_sum =  Organization.objects.filter(org_special=True).filter(
            ReferringEntity__PatientVisit__visit_date__range=(start_date,end_date)).annotate(
            total_org_special_visits=Sum('ReferringEntity__PatientVisit__visit_count')
            ).order_by('-total_org_special_visits')[:5]

        patient_visits = PatientVisit.objects.filter(visit_date__range=[LAST_12_MONTH,LAST_MONTH])

        if patient_visits:
            try:
                patient_visits = patient_visits.extra(select={'month': 'STRFTIME("%m",visit_date)'})
                print (patient_visits[0].month)
            except Exception:
                patient_visits = patient_visits.extra(select={'month': 'EXTRACT(month FROM visit_date)'})
            patient_visits = patient_visits.values('month').annotate(total_visit_count=Sum('visit_count'))

            for patient_visit in patient_visits:
                if LAST_MONTH.month <= int(patient_visit['month']) :
                    current_month = date(day=LAST_MONTH.day, month= int(patient_visit['month']), year=LAST_MONTH.year)
                else:
                    current_month = date(day=LAST_12_MONTH.day, month= int(
                        patient_visit['month']), year=LAST_12_MONTH.year)

                last_month = current_month-timedelta(days=364)
                patient_visits_year = PatientVisit.objects.filter(
                    visit_date__range=[last_month, current_month]).aggregate(year_total=Sum('visit_count'))
                patient_visit['year_total'] = patient_visits_year['year_total']
                patient_visit['year_from'] = last_month
                patient_visit['year_to'] = current_month
        today = date.today()
        week_ago = today - timedelta(days=7)
        all_orgs = ReferringEntity.objects.order_by('entity_name')
        all_ref = {}
        for phys in all_orgs :
            phys_ref = phys.get_patient_visit({'from_date' : week_ago, 'to_date' : today});
            if phys_ref.count() :
                for ref in phys_ref :
                    if not phys.id in all_ref :
                        all_ref[phys.id] = {'name' : phys.entity_name, 'refs' :  [ ref ] }
                    else :
                        all_ref[phys.id]['refs'].append(ref)

        ctx = {
            "orgform": orgform,
            "phyform": phyform,
            "refform": refform,
            "referring_entity_visit_sum": referring_entity_visit_sum,
            "org_visit_sum": org_visit_sum,
            "special_visit_sum": special_visit_sum,
            "patient_visits": patient_visits,
            "all_orgs": all_ref,
            'today': today,
            'week_ago': week_ago,
            'timezone': TIME_ZONE,
        }
        ctx.update(initial_ctx or {})
        return ctx

    def get(self, request, *args, **kwargs):
        ctx = self.get_context()
        return render(request, "index.html", ctx)

    def post(self, request, *args, **kwargs):

        phyform = ReferringEntityForm()
        orgform = OrganizationForm()
        refform = PatientVisitForm()

        if 'phyform' in request.POST:
            phyform = ReferringEntityForm(request.POST)
            if phyform.is_valid():
                phyform.save()
                return redirect(reverse('index'))

        elif 'orgform' in request.POST:
            orgform = OrganizationForm(request.POST)
            if orgform.is_valid():
                orgform.save()
                return redirect(reverse('index'))

        elif 'refform' in request.POST:
            refform = PatientVisitForm(request.POST)
            if refform.is_valid():
                refform.save()
                return redirect(reverse('index'))

        ctx = self.get_context(initial_ctx={
            "orgform": orgform,
            "phyform": phyform,
            "refform": refform,
        })

        return render(request, "index.html", ctx)


class OrganizationView(LoginRequiredMixin, View):
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
            return redirect(reverse('add-referring-entity'))

        return render(request,"tracking/organization.html",ctx )


class ReferringEntityView(LoginRequiredMixin, View):
    # display the referring_entity form
    def get(self, request, *args, **kwargs):
        form = ReferringEntityForm()
        ctx = {"form": form}
        return render(request,"tracking/referring_entity.html",ctx )


    def post(self, request, *args, **kwargs):
        form = ReferringEntityForm(request.POST)
        if form.is_valid():
            form.save()
            form = ReferringEntityForm()

        ctx = {"form": form}
        return render(request,"tracking/referring_entity.html",ctx )

class TreatingProviderView(LoginRequiredMixin, View):
    # display the treating_provider form
    def get(self, request, *args, **kwargs):
        form = TreatingProviderForm()
        ctx = {"form": form}
        return render(request,"tracking/treating_provider.html",ctx )


    def post(self, request, *args, **kwargs):
        form = TreatingProviderForm(request.POST)
        if form.is_valid():
            form.save()
            form = TreatingProviderForm()

        ctx = {"form": form}
        return render(request,"tracking/treating_provider.html",ctx )


class PatientVisitView(LoginRequiredMixin, View):
    # display the patient_visit form
    def get(self, request, *args, **kwargs):
        form = PatientVisitForm()
        ctx = {"form": form, 'timezone': TIME_ZONE}
        return render(request,"tracking/patient_visit.html",ctx )

    def post(self, request, *args, **kwargs):
        form = PatientVisitForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add/patient_visit/')
        ctx = {"form": form, 'timezone': TIME_ZONE}
        return render(request,"tracking/patient_visit.html",ctx )

class GetPatientVisitReport(LoginRequiredMixin, View):
    """
    Display a summary of patient_visits by Organization:provider:
    """
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
        return render(request, "tracking/show_patient_visit_report.html", ctx)


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('/')


class GetPatientVisitHistory(LoginRequiredMixin, View):
    """
    Display a summary of patient_visits by Date:ReferringEntity:Organization:Count:
    """
    def get(self, request, *args, **kwargs):
        today = date.today()
        patient_visits = PatientVisit.objects.filter(visit_date=today).order_by('-visit_date')
        form = PatientVisitHistoryForm(initial={'from_date': today, 'to_date' : today})
        ctx = {
                'patient_visits': patient_visits,
                'timezone': TIME_ZONE,
                "form": form
            }
        return render(request,"tracking/show_patient_visit_history.html",ctx )


    def post(self, request, *args, **kwargs):

        form = PatientVisitHistoryForm(request.POST)
        if form.is_valid():
            cleaned_data = form.clean()
            patient_visits = PatientVisit.objects\
                .filter(visit_date__gte=cleaned_data['from_date'])\
                .filter(visit_date__lte=cleaned_data['to_date'])\
                .order_by('-visit_date')
            if cleaned_data['referring_entity']:
                patient_visits = patient_visits.filter(referring_entity__in=cleaned_data['referring_entity'])
        else:
            patient_visits = []

        ctx = {
            'patient_visits': patient_visits,
            'timezone': TIME_ZONE,
            "form": form
        }
        return render(request,"tracking/show_patient_visit_history.html",ctx )


@login_required
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


@login_required
def edit_referring_entity(request, referring_entity_id):
    referring_entity = get_object_or_404(ReferringEntity, id=referring_entity_id)
    if request.method == 'POST':
        form = ReferringEntityForm(request.POST, instance=referring_entity)
        if form.is_valid():
            form.save()
            return render(request, 'tracking/referring_entity_edit.html', {
                'form': form,
                'success': True})

    else:
        form = ReferringEntityForm(instance=referring_entity)

    return render(request, 'tracking/referring_entity_edit.html', {'form': form})


@login_required
def edit_treating_provider(request, treating_provider_id):
    treating_provider = get_object_or_404(TreatingProvider, id=treating_provider_id)
    if request.method == 'POST':
        form = TreatingProviderForm(request.POST, instance=treating_provider)
        if form.is_valid():
            form.save()
            return render(request, 'tracking/treating_provider_edit.html', {
                'form': form,
                'success': True})

    else:
        form = TreatingProviderForm(instance=treating_provider)

    return render(request, 'tracking/treating_provider_edit.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def delete_referring_entity(request, referring_entity_id):
    ''' delete a referring_entity '''

    referring_entity = get_object_or_404(ReferringEntity,
                                         id=referring_entity_id)
    form = GenericDeleteForm(request.POST)
    if form.is_valid():
        referring_entity.delete()
        messages.success(request, 'Entity deleted successfully.')

    next = request.META.get('HTTP_REFERER') or \
        reverse('view-referring-entities')

    return redirect(next)


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'tracking/organization_list.html'
    context_object_name = "organizations"
    paginate_by = 10


class ReferringEntityListView(LoginRequiredMixin, ListView):
    model = ReferringEntity
    template_name = 'tracking/referring_entity_list.html'
    context_object_name = "referring_entitys"
    paginate_by = 10

class TreatingProviderListView(LoginRequiredMixin, ListView):
    model = TreatingProvider
    template_name = 'tracking/treating_provider_list.html'
    context_object_name = "treating_providers"
    paginate_by = 10
