from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SetupAdminSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'is_active', 'date_joined']


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']

    def validate_user_type(self, value):
        if value == 'admin':
            raise serializers.ValidationError('Cannot create admin users through this endpoint.')
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'is_active']

    def validate_user_type(self, value):
        if value == 'admin':
            raise serializers.ValidationError('Cannot assign admin role through this endpoint.')
        return value
