import io

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.apps import apps


class MainPageView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        s3_service = apps.get_app_config("cloud").s3_service

        current_path = request.GET.get("path", "").strip("/")

        user_objects = s3_service.get_objects(request.user.id, current_path)

        return render(
            request,
            "cloud/layouts/index.html",
            context={
                "user_objects": user_objects,
                "current_path": current_path,
                "breadcrumb": current_path.split('/')
            },
        )

    def post(self, request, *args, **kwargs):
        s3_service = apps.get_app_config("cloud").s3_service

        files = zip(
            request.FILES.getlist("fileList"),
            request.POST.getlist("filePaths"),
        )

        current_path = request.GET.get("path")

        for file, full_path in files:
            s3_service.create_object(
                request.user.id, full_path, current_path, io.BytesIO(file.read())
            )

        return redirect("cloud:main")
