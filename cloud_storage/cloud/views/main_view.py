from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.http.response import HttpResponse

from ..s3_service.exceptions import ObjectNameError


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

        files = request.FILES.getlist("fileList")

        current_path = request.GET.get("path", "").strip("/")

        try:
            s3_service.upload_objects(request.user.id, files, current_path)
        except ObjectNameError:
            return HttpResponse(status=400)

        return redirect("cloud:main")
