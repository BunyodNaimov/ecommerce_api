from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import CustomUser
from users.serializers import RegisterSerializers, LoginSerializers, CustomTokenObtainPairSerializer, UserSerializer


class RegisterView(APIView):
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
