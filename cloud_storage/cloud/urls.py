from django.urls import path

from .views.main_page_view import MainPageView
from .views.search_page_view import SearchPageView

from .views.object_handling_view import S3ObjectHandlingView


urlpatterns = [
    path("", MainPageView.as_view(), name="main"),
    path("upload_object/", MainPageView.as_view(), name="upload_object"),
    path("create_object/", S3ObjectHandlingView.as_view(), name="create_object"),
    path("delete_object/", S3ObjectHandlingView.as_view(), name="delete_object"),
    path("rename_object/", S3ObjectHandlingView.as_view(), name="rename_object"),
    path("download_object/", S3ObjectHandlingView.as_view(), name="download_object"),
    path("search/", SearchPageView.as_view(), name="search"),
]
