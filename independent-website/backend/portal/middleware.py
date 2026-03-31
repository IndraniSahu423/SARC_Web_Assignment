from types import SimpleNamespace

from django.http import JsonResponse

from .auth_client import verify_token_with_auth_service


class TokenVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = {
            "/",
            "/api/portal/register/",
            "/admin/",
        }

    def __call__(self, request):
        if request.path in self.exempt_paths or request.path.startswith("/admin/"):
            return self.get_response(request)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JsonResponse({"detail": "Authorization token missing or invalid."}, status=401)

        token = auth_header.split(" ", 1)[1].strip()
        identity = verify_token_with_auth_service(token)
        if not identity:
            return JsonResponse({"detail": "Invalid or expired token."}, status=401)

        request.user_identity = SimpleNamespace(**identity)
        return self.get_response(request)
