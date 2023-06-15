from django.urls import path, include
from rest_framework import routers

from app import views

app_name = 'app'

router = routers.DefaultRouter()
router.register(r"tasks", views.TaskApiView, basename="tasks")

urlpatterns = [
    path("", include(router.urls)),
]
