from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import CustomUser, VerificationCode
from users.serializers import RegisterSerializers, LoginSerializers, CustomTokenObtainPairSerializer, UserSerializer, \
    UserDetailSerializer, SendEmailVerificationCodeSerializer, CheckEmailVerificationCodeSerializers


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializers)
    def post(self, request, *args, **kwargs):
        serializers = RegisterSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserDetailSerializer)
    def put(self, request, *args, **kwargs):
        serializers = UserDetailSerializer(instance=request.user, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializers = LoginSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        email = serializers.validated_data.get('email')
        password = serializers.validated_data.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            authenticate(request, password=password, email=email)
            return Response(serializers.data)
        else:
            raise Http404


class SendEmailVerificationCodeView(APIView):
    queryset = VerificationCode.objects.all()

    @swagger_auto_schema(request_body=SendEmailVerificationCodeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SendEmailVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = get_random_string(allowed_chars='0123456789', length=6)
        VerificationCode.objects.update_or_create(email=email, defaults={'code': code, 'is_verified': False}, )
        message = f"Email tasdiqlash kodingiz {code}"
        subject = 'Email registration'
        send_mail(
            subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email]
        )
        return Response({"detail": "Successfully send email verification code."})


class CheckEmailVerificationCodeView(CreateAPIView):
    queryset = VerificationCode.objects.all()
    serializer_class = CheckEmailVerificationCodeSerializers

    def create(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        email = serializers.validated_data.get('email')
        code = serializers.validated_data.get('code')
        verification_code = self.get_queryset().filter(email=email, is_verified=False).order_by(
            '-last_sent_time').first()
        if verification_code and verification_code.code != code:
            raise ValidationError("Verification code invalid.")
        verification_code.is_verified = True
        verification_code.save(update_fields=['is_verified'])
        return Response({"detail": "Verification code is verified"})
