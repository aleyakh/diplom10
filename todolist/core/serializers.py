from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from todolist.core.fields import PasswordField
from todolist.core.models import User
from django.contrib.auth import authenticate


class CreateUserSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError({'password_repeat': 'Password must match'})
        return attrs

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')
        read_only_fields = ('id', 'first_name', 'last_name', 'email')

    def create(self, validated_data: dict) -> User:
        if user := authenticate(
            username=validated_data['username'],
            password=validated_data['password']
        ):
            return user
        raise AuthenticationFailed


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')
