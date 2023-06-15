import re

from rest_framework import serializers

from app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


    # def validate_phone(self, phone: str):
    #     pattern_phone = r"^[7]{1}[0-9]{10}$"
    #     if re.match(pattern_phone, phone) is None:
    #         raise serializers.ValidationError("Неверный формат phone")
    #     return phone
    #
    # def validate_telegram_id(self, tg_id: str):
    #     pattern_phone = r"^[7]{1}[0-9]{10}$"
    #     if re.match(pattern_phone, tg_id) is None:
    #         raise serializers.ValidationError("Неверный формат telegram_id")
    #     return tg_id
