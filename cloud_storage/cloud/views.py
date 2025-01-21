import io

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.apps import apps


class MainPageView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        s3_service = apps.get_app_config("cloud").s3_service

        current_path = request.GET.get("path")

        user_objects = sorted(s3_service.get_objects(request.user.id, current_path), key=lambda x: not x.is_dir)

        return render(request, "cloud/layouts/index.html", context={'user_objects': user_objects})

    def post(self, request, *args, **kwargs):
        s3_service = apps.get_app_config("cloud").s3_service

        file = request.FILES.get("file")
        current_path = request.GET.get("path")

        if file:
            object_name = request.FILES.get("file").name
            object_bytes = io.BytesIO(request.FILES.get("file").read())

            s3_service.create_object(
                request.user.id, object_name, current_path, object_bytes
            )

        return redirect("cloud:main")
