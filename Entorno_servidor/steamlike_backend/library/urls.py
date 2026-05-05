from django.urls import path
from . import views

urlpatterns = [
    path("entries/", views.library_entries, name="library-entries"),
    path("entries/<int:id>/", views.library_entry_by_id, name="library-entry-by-id"),
    path("", views.health, name="health"),
]
