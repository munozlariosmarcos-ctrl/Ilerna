from django.contrib import admin
from django.urls import path, include
from library.views import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/library/", include("library.urls")),
    path("api/health/", health),
    path("api/auth/", include("accounts.urls")),
    path("api/users/", include("accounts.urls_users")),
]
