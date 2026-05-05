from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", include("library.urls_health")),
    path("api/library/", include("library.urls")),
    path("api/auth/", include("accounts.urls")),
    path("api/users/", include("accounts.urls_users")),
    path("api/catalog/", include("catalog.urls")),
    path("api/debug/", include("debug.urls")),
    path("", TemplateView.as_view(template_name="index.html"), name="frontend"),
]