from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from users.forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
# from django.contrib.auth import authenticate, login


class RegisterView(View):
    # display the referral form

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        ctx = {"form": form}
        return render(request, "registration/register.html", ctx)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        password = request.POST.get('password')
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(password)
            user.save()
            messages.success(request, 'User Succefully registered.')
            return HttpResponseRedirect('/')
        ctx = {"form": form}
        return render(request, "registration/register.html", ctx)


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        ctx = {"form": form}
        return render(request, "tracking/login.html", ctx)

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        username = request.POST.get('username', None)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return HttpResponseRedirect(request.GET.get('next') or '/home')
        else:
            if username:
                message = list(form.errors.values())[0]
            else:
                message = ""
            messages.warning(request, message)

        ctx = {"form": form}
        return render(request, "tracking/login.html", ctx)
