from rest_framework import serializers


class PortalRegisterRelaySerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    name = serializers.CharField(max_length=255)
    roll_number = serializers.CharField(max_length=50)
    hostel_number = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True, min_length=6)
