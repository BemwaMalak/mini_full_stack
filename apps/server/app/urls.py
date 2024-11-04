from django.urls import include, path

urlpatterns = [path("api/", include([path("auth/", include("authentication.urls"))]))]
