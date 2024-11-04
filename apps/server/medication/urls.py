from django.urls import path
from .views import MedicationApiView

urlpatterns = [
    path("", MedicationApiView.as_view(), name="medication-list-create"),
    path(
        "<int:pk>/",
        MedicationApiView.as_view(),
        name="medication-detail-update",
    ),
]
