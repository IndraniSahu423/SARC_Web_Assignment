from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "name", "roll_number", "hostel_number", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError("Invalid username or password.") from exc

        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid username or password.")

        attrs["user"] = user
        return attrs
