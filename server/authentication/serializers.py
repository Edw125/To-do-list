from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "phone", "telegram_id")
        extra_kwargs = {
            "phone": {"required": False, "allow_null": True},
            "telegram_id": {"required": False, "allow_null": True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            telegram_id=validated_data.get('telegram_id'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user
