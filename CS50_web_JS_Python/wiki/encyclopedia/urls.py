from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("edit/<str:name>", views.edit, name="edit"),
    path('wiki/<str:name>', views.showMD, name="showMD")
]
