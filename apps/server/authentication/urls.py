from django.urls import path

from .views import LoginApiView, LogoutApiView, RegisterApiView, UserInfoApiView

urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="register"),
    path("login/", LoginApiView.as_view(), name="login"),
    path("logout/", LogoutApiView.as_view(), name="logout"),
    path('user-info/', UserInfoApiView.as_view(), name='user-info'),
]
