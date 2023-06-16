from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.serializers import UserSerializer, UserCheckerSerializer, UserUpdateSerializer

User = get_user_model()


class UserRegisterApiView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserUpdateApiView(generics.GenericAPIView):
    serializer_class = UserUpdateSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTgCheckerApiView(APIView):
    serializer_class = UserCheckerSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserCheckerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data.get("phone")
            telegram_id = serializer.validated_data.get("telegram_id")

            user = User.objects.filter(phone=phone, telegram_id=telegram_id).first()
            if not user:
                return Response({'detail': "User not found"}, status=status.HTTP_404_NOT_FOUND)
            jwt_token = RefreshToken.for_user(user)
            tokens = {
                "refresh": str(jwt_token),
                "access": str(jwt_token.access_token)
            }
            return Response(tokens, status=status.HTTP_200_OK)
