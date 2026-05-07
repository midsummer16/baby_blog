from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


INVITATION_CODE = 'kongkong'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=3)
    password2 = serializers.CharField(write_only=True, min_length=3)
    invitation_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'invitation_code']

    def validate_invitation_code(self, value):
        if value != INVITATION_CODE:
            raise serializers.ValidationError('邀请码不正确')
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data.pop('invitation_code')
        password = validated_data.pop('password')
        user = User(**validated_data, role='normal')
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'avatar', 'bio', 'phone', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'bio', 'phone', 'avatar']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=3)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('旧密码不正确')
        return value
