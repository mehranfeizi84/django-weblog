from django.contrib.auth import views
from django.urls import path
from .views import (
        HomeAccount,
        CreateArticle,
        UpdateArticle,
        DeleteArticle ,
        Profile,

        )


app_name = 'account'
urlpatterns = [
    path("", HomeAccount.as_view(), name="home"),
    path("article/create", CreateArticle.as_view(), name="create-article"),
    path("article/update/<int:pk>", UpdateArticle.as_view(), name="update-article"),
    path("article/delete/<int:pk>", DeleteArticle.as_view(), name="delete-article"),
    path("profile/", Profile.as_view(), name="profile"),
]
