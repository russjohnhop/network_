
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API routes
    path("posts/<int:post_id>", views.post, name="post"),
    path("posts/like/<int:post_id>", views.update_likes, name="update_likes"),
]

# Looking at how mail used the api to figure out how to do it