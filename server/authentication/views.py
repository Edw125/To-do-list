from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers import UserSerializer


class UserRegisterApiView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
