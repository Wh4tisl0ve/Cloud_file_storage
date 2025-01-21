from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include(('users.urls', 'users'), namespace='accounts')),
    path("", include(('cloud.urls', 'cloud'), namespace='cloud'))
]
