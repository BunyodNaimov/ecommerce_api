from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'full_name', 'phone')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'phone')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('first_name', None)
        data.pop('last_name', None)
        data['full-name'] = instance.get_full_name()
        return data


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["access"] = str(refresh.access_token)
        data["refresh"] = str(refresh)
        data["user"] = UserSerializer(self.user).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegisterSerializers(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'password1', 'password2')
        read_only_fields = ('id',)

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.pop('password2', None)
        if password2 != password1:
            raise ValidationError(_("Password didn't match. "))
        return super().validate(attrs)

    def create(self, validated_data):
        password1 = validated_data.pop('password1', None)
        user = CustomUser(**validated_data)
        user.set_password(password1)
        user.save()
        return user


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class SendEmailVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CheckEmailVerificationCodeSerializers(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
