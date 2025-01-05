from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import RegisterForm


class RegistrationPageView(TemplateView):
    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        register_form = RegisterForm()
        return render(request, self.template_name, {"form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save(commit=True)
            return redirect("users:login")

        return render(request, self.template_name, {"form": register_form})
