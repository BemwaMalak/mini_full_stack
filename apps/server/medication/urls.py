from django.urls import path

from .views import MedicationApiView, RefillRequestApiView

urlpatterns = [
    path("", MedicationApiView.as_view(), name="medication-list-create"),
    path(
        "<int:pk>/",
        MedicationApiView.as_view(),
        name="medication-detail-update",
    ),
    path("refill-request/", RefillRequestApiView.as_view(), name="refill-request-list-create"),
    path(
        "refill-request/<int:pk>/",
        RefillRequestApiView.as_view(),
        name="refill-request-detail-update",
    ),
]
