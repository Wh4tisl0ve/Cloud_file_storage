import io, json

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.apps import apps


class S3ObjectHandlingView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        s3_service = apps.get_app_config("cloud").s3_service
        
        request_body = json.loads(request.body.decode('utf-8'))
        object_name = request_body.get('nameFolder')

        current_path = request.GET.get("path")

        s3_service.create_object(request.user.id, object_name, current_path)
        
        return redirect("cloud:main")

    def patch(self, request, *args, **kwargs):
        return redirect("cloud:main")

    def delete(self, request, *args, **kwargs):
        return redirect("cloud:main")
