from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from app import serializers
from app.models import Task


class TaskApiView(viewsets.ModelViewSet):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
