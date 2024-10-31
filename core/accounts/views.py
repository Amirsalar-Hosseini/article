from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer


class UserRegisterView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        ser_data = self.serializer_class(instance=user, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
