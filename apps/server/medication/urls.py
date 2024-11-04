from django.urls import path

from .views import MedicationApiView, RefillRequestApiView

urlpatterns = [
    path("", MedicationApiView.as_view(), name="medication-list-create"),
    path(
        "<int:pk>/",
        MedicationApiView.as_view(),
        name="medication-detail-update",
    ),
    path("refill/", RefillRequestApiView.as_view(), name="refillrequest-list-create"),
    path(
        "refill/<int:pk>/",
        RefillRequestApiView.as_view(),
        name="refillrequest-detail-update",
    ),
]
