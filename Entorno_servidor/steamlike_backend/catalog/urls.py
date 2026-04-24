from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.search, name="catalog-search"),
    path("resolve/", views.resolve, name="catalog-resolve"),  # ← añadir
]