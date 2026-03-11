from django.urls import path
from .views import *


urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("passes/types/", PassTypesView.as_view()),
    path("passes/purchase/", PurchasePassView.as_view()),
    path("validate/", ValidatePass.as_view()),
    path("trips/history/", TripHistory.as_view()),
    path("admin/dashboard/", AdminDashboard.as_view()),
    path("transport-mode/create", CreateTransportMode.as_view()),
    path("pass-type/create", CreatePassType.as_view()),
]
