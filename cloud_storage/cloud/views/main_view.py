import io

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps


class MainPageView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        s3_service = apps.get_app_config("cloud").s3_service

        current_path = request.GET.get("path", "").strip("/")

        user_objects = s3_service.get_objects(request.user.id, current_path)

        path = ""
        breadcrumb = []
        for page in current_path.split("/"):
            path += f"{page}/"
            breadcrumb.append((path, page))

        page_number = request.GET.get("page", 1)
        page_obj = Paginator(user_objects, 10).get_page(page_number)

        return render(
            request,
            "cloud/layouts/index.html",
            context={
                "page_obj": page_obj,
                "current_path": current_path,
                "breadcrumb": breadcrumb,
            },
        )

    def post(self, request, *args, **kwargs):
        s3_service = apps.get_app_config("cloud").s3_service

        files = zip(
            request.FILES.getlist("fileList"),
            request.POST.getlist("filePaths"),
        )

        current_path = request.GET.get("path", "").strip("/")

        for file, full_path in files:
            s3_service.create_object(
                request.user.id, full_path, current_path, io.BytesIO(file.read())
            )

        return redirect("cloud:main")
