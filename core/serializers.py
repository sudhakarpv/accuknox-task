from rest_framework import serializers
from .models import User, FriendRequest
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import status


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "name")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data["name"]
        )
        return user


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "name")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name')


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'accepted',
                  'rejected', 'created_at')
