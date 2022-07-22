from django.contrib.auth import views
from django.urls import path
from .views import (
        HomeAccount,
        CreateArticle,
        UpdateArticle,
        DeleteArticle ,
        Profile,
        CommentList,
        UpdateComment,
        DeleteComment,
        CommentsArticleList,
        )


app_name = 'account'
urlpatterns = [
    path("", HomeAccount.as_view(), name="home"),
    path("article/create", CreateArticle.as_view(), name="create-article"),
    path("article/update/<int:pk>", UpdateArticle.as_view(), name="update-article"),
    path("article/delete/<int:pk>", DeleteArticle.as_view(), name="delete-article"),
    path("profile/", Profile.as_view(), name="profile"),
    path("comments/", CommentList.as_view(), name="comments"),
    path("comments/update/<int:pk>", UpdateComment.as_view(), name="update-comment"),
    path("comments/delete/<int:pk>", DeleteComment.as_view(), name="delete-comment"),
    path("comments/article/<int:pk>", CommentsArticleList.as_view(), name="comments-article"),
]
