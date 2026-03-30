from django.urls import path

from .views import DashboardView, PortalRegisterView

urlpatterns = [
    path("register/", PortalRegisterView.as_view(), name="portal-register"),
    path("dashboard/", DashboardView.as_view(), name="portal-dashboard"),
]
