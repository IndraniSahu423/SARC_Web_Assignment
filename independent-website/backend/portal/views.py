import os

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LocalUserProfile
from .serializers import PortalRegisterRelaySerializer


class PortalRegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PortalRegisterRelaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        base_url = os.getenv("AUTH_SERVICE_URL", "http://localhost:8000").rstrip("/")
        register_url = f"{base_url}/api/auth/register/"

        try:
            auth_response = requests.post(
                register_url,
                json=serializer.validated_data,
                timeout=8,
            )
        except requests.RequestException:
            return Response(
                {"detail": "Failed to contact auth service."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if auth_response.status_code not in (200, 201):
            try:
                payload = auth_response.json()
            except ValueError:
                payload = {"detail": "Auth service returned an invalid response."}
            return Response(payload, status=auth_response.status_code)

        payload = serializer.validated_data
        LocalUserProfile.objects.update_or_create(
            roll_number=payload["roll_number"],
            defaults={
                "name": payload["name"],
                "hostel_number": payload["hostel_number"],
            },
        )

        return Response(
            {
                "success": True,
                "message": "User registered via centralized auth service.",
            },
            status=status.HTTP_201_CREATED,
        )


class DashboardView(APIView):
    def get(self, request):
        identity = getattr(request, "user_identity", None)
        if not identity:
            return Response({"detail": "Unauthorized."}, status=status.HTTP_401_UNAUTHORIZED)

        profile, _ = LocalUserProfile.objects.get_or_create(
            roll_number=identity.roll_number,
            defaults={
                "name": identity.name,
                "hostel_number": "",
            },
        )

        if profile.name != identity.name:
            profile.name = identity.name
            profile.save(update_fields=["name", "updated_at"])

        return Response(
            {
                "roll_number": profile.roll_number,
                "name": profile.name,
                "hostel_number": profile.hostel_number,
                "bio": profile.bio,
                "year_of_study": profile.year_of_study,
            },
            status=status.HTTP_200_OK,
        )
