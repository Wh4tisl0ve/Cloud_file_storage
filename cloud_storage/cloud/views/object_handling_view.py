import json

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.http.response import HttpResponse


class S3ObjectHandlingView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        s3_service = apps.get_app_config("cloud").s3_service

        request_body = json.loads(request.body.decode("utf-8"))
        object_name = request_body.get("nameObject")

        current_path = request.GET.get("path", "").strip("/")

        s3_service.create_object(request.user.id, object_name, current_path)

        return HttpResponse(status=201)

    def patch(self, request, *args, **kwargs):
        s3_service = apps.get_app_config("cloud").s3_service

        request_body = json.loads(request.body.decode("utf-8"))
        old_name = request_body.get("oldName")
        new_name = request_body.get("newName")

        current_path = request.GET.get("path", "").strip("/")

        s3_service.rename_object(request.user.id, old_name, new_name, current_path)

        return HttpResponse(status=200)

    def delete(self, request, *args, **kwargs):
        s3_service = apps.get_app_config("cloud").s3_service

        request_body = json.loads(request.body.decode("utf-8"))
        object_name = request_body.get("nameObject")

        current_path = request.GET.get("path", "").strip("/")

        s3_service.delete_object(request.user.id, object_name, current_path)

        return HttpResponse(status=204)
