from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from permissions import IsVerify
from .models import User, VerificationCode
from .serializers import UserSerializer
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.core.mail import send_mail
# from django.urls import reverse
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.contrib.auth import get_user_model
# from django.utils.http import urlsafe_base64_decode
# from rest_framework import serializers


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
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        user = self.queryset.get(id=request.user.id)
        ser_data = self.serializer_class(instance=user, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationCodeView(APIView):
    permission_classes = (IsVerify, IsAuthenticated)
    queryset = VerificationCode.objects.all()

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        last_code = self.queryset.filter(user=user).order_by('-created_at').first()

        if last_code and last_code.created > timezone.now() - timezone.timedelta(minutes=1):
            return Response({'error': 'You can only request a code once per minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        code = VerificationCode.generate_code()
        VerificationCode.objects.create(user=user, code=code)

        return Response({'message': 'Verification code sent.'}, status=status.HTTP_200_OK)


class VerifyCodeView(APIView):
    permission_classes = (IsVerify, IsAuthenticated)
    queryset = VerificationCode.objects.all()

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        code = request.data.get('code')

        last_code = self.queryset.filter(user=user, is_used=False).order_by('-created_at').first()

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



class UserLogOutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request):
        user = self.queryset.get(id=request.user.id)
        ser_data = self.serializer_class(user)
        return Response(ser_data.data, status=status.HTTP_200_OK)

#
# User = get_user_model()
#
# # not confirm (need to testtttttttttttttttttttttt)
# class PasswordResetRequestView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         token_generator = PasswordResetTokenGenerator()
#         token = token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         reset_link = request.build_absolute_uri(
#             reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
#         )
#
#         send_mail(
#             subject="Password Reset Request",
#             message=f"Click the link to reset your password: {reset_link}",
#             from_email="your_email@gmail.com",
#             recipient_list=[user.email]
#         )
#
#         return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
#
# # not confirm (need to testtttttttttttttttttttttt)
# class PasswordResetConfirmView(APIView):
#     class PasswordResetSerializer(serializers.Serializer):
#         password = serializers.CharField(write_only=True)
#
#     def post(self, request, uidb64, token):
#         serializer = self.PasswordResetSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 uid = urlsafe_base64_decode(uidb64).decode()
#                 user = User.objects.get(pk=uid)
#             except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#                 return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)
#
#             if PasswordResetTokenGenerator().check_token(user, token):
#                 user.set_password(serializer.validated_data['password'])
#                 user.save()
#                 return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)