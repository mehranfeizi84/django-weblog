from django.contrib.auth import views
from django.urls import path
from .views import (
        home,
        ArticlesList,
        CreateArticle,
        UpdateArticle,
        DeleteArticle ,
        Profile,
        CommentList,
        UpdateComment,
        DeleteComment,
        CommentsArticleList,
        UsersList,
        UpdateUser,
        DeleteUser,
        )


app_name = 'account'
urlpatterns = [
    path("", home, name="home"),
    path("articles", ArticlesList.as_view(), name="articles"),
    path("article/create", CreateArticle.as_view(), name="create-article"),
    path("article/update/<int:pk>", UpdateArticle.as_view(), name="update-article"),
    path("article/delete/<int:pk>", DeleteArticle.as_view(), name="delete-article"),
    path("profile/", Profile.as_view(), name="profile"),
    path("comments/", CommentList.as_view(), name="comments"),
    path("comments/update/<int:pk>", UpdateComment.as_view(), name="update-comment"),
    path("comments/delete/<int:pk>", DeleteComment.as_view(), name="delete-comment"),
    path("comments/article/<int:pk>", CommentsArticleList.as_view(), name="comments-article"),
    path("users", UsersList.as_view(), name="users"),
    path("users/update/<int:pk>", UpdateUser.as_view(), name="update-user"),
    path("users/delete/<int:pk>", DeleteUser.as_view(), name="delete-user"),
]
