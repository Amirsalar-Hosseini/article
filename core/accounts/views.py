from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from permissions import IsVerify
from .models import User, VerificationCode
from .serializers import UserSerializer
from django.utils import timezone


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


class SendVerificationCodeView(APIView):
    permission_classes = (IsVerify,)

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        last_code = VerificationCode.objects.filter(user=user).order_by('-created_at').first()

        if last_code and last_code.created > timezone.now() - timezone.timedelta(minutes=1):
            return Response({'error': 'You can only request a code once per minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        code = VerificationCode.generate_code()
        VerificationCode.objects.create(user=user, code=code)

        return Response({'message': 'Verification code sent.'}, status=status.HTTP_200_OK)


class VerifyCodeView(APIView):
    permission_classes = (IsVerify,)

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        code = request.data.get('code')

        last_code = VerificationCode.objects.filter(user=user, is_used=False).order_by('-created_at').first()

        if not last_code:
            return Response({'error': 'No verification code found.'}, status=status.HTTP_404_NOT_FOUND)

        if not last_code.is_valid():
            return Response({'error': 'The verification code has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        if last_code.code == code:
            last_code.is_used = True
            last_code.save()
            user.is_verify = True
            user.save()
            return Response({'message': 'Phone number verification complete.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)