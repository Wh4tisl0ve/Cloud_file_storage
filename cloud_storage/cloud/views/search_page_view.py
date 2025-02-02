from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps


class SearchPageView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        s3_service = apps.get_app_config("cloud").s3_service

        query_string = request.GET.get("query", "")

        finding_objects = s3_service.find_objects(request.user.id, query_string)
        name_files = []
        directory_files = []

        for obj in finding_objects:
            parts = obj.object_name.rstrip('/').split('/')
            current_object = f"{parts[-1]}/" if obj.is_dir else parts[-1]

            name_files.append(current_object)
            directory_files.append("/".join(parts[:-1]))

        object_info = zip(finding_objects, name_files, directory_files)

        return render(
            request,
            "cloud/layouts/search.html",
            context={
                "objects": object_info,
            },
        )
