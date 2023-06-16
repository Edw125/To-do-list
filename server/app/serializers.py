
from rest_framework import serializers

from app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        extra_kwargs = {'user': {'required': False}}
