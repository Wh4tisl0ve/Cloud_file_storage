from django.urls import path

from .views.main_view import MainPageView
from .views.object_handling_view import S3ObjectHandlingView


urlpatterns = [
    path("", MainPageView.as_view(), name="main"),
    path("create_object/", S3ObjectHandlingView.as_view(), name="create_object"),
    path("delete_object/", S3ObjectHandlingView.as_view(), name="delete_object"),
    path("update_object/", S3ObjectHandlingView.as_view(), name="update_object"),
    # path('search/', SearchPageView.as_view(), name='search')
]
