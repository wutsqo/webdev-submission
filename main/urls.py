from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("post/<slug:slug>", views.detail, name="detail"),
    path("login/", LoginView.as_view(template_name="main/login.html"), name="login"),
    path("register/", views.register, name="register"),
    path(
        "logout/", LogoutView.as_view(template_name="main/logout.html"), name="logout"
    ),
    path("new/", views.add_post, name="new"),
]
