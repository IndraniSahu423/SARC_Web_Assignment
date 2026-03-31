from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse

# Root endpoint that returns a simple message
def root_view(request):
    return JsonResponse({
        "message": "SARC Portal Backend Running",
        "version": "1.0.0",
        "endpoints": {
            "register": "/api/portal/register/",
            "dashboard": "/api/portal/dashboard/",
        }
    })

urlpatterns = [
    path("", root_view, name="root"),
    path("admin/", admin.site.urls),
    path("api/portal/", include("portal.urls")),
]
