from django.urls import path

from chat import views

urlpatterns = [
    path("settings/", views.settings, name="settings"),
    path("key/<str:model>/", views.key, name="key"),
]
