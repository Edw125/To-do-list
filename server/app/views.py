from rest_framework import viewsets

from app import serializers
from app.models import Task


class TaskApiView(viewsets.ModelViewSet):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(seller=self.request.user)
        return queryset
