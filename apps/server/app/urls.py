from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path(
        "api/",
        include(
            [
                path("auth/", include("authentication.urls")),
                path("medication/", include("medication.urls")),
            ]
        ),
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)