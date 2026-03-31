from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse

# Root endpoint that returns a simple message
def root_view(request):
    return JsonResponse({
        "message": "SARC Auth Service Running",
        "version": "1.0.0",
        "endpoints": {
            "register": "/api/auth/register/",
            "login": "/api/auth/login/",
            "verify": "/api/auth/verify/",
        }
    })

urlpatterns = [
    path("", root_view, name="root"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentication.urls")),
]
