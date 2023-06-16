from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "phone", "telegram_id")
        extra_kwargs = {
            "phone": {"required": True, "allow_null": True},
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


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone", "telegram_id", "first_name", "last_name")


class UserCheckerSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=25)
    telegram_id = serializers.CharField(max_length=25)

    def validate_phone(self, phone):
        phone = validate_phone(phone)
        if len(phone) < 12:
            raise serializers.ValidationError("Неверный формат телефона.")
        return phone


def validate_phone(phone):
    phone = phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    if phone.startswith("8"):
        phone = "+7" + phone[1:]
    elif phone.startswith("9"):
        phone = "+7" + phone
    elif not phone.startswith("+"):
        phone = "+" + phone
    return phone
