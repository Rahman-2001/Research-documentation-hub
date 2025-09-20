from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("about_page", views.about, name="about"),
    path("contact_page", views.contact, name="contact"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    # path("post/detail", views.detail, name="detail")  
    path("post/<str:slug>", views.detail, name="post_detail"),
    path("old_url", views.old_url_redirect, name="old_url"),
    path("new_test_url", views.new_url, name="new_url_usingname"),
    path("new_post", views.new_post, name="new_post"),

]  
