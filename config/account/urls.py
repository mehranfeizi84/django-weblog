from django.contrib.auth import views
from django.urls import path
from .views import (
        AllCommentList,
        Home,
        ArticlesList,
        CreateArticle,
        UpdateArticle,
        DeleteArticle ,
        Profile,
        MyCommentList,
        UpdateComment,
        DeleteComment,
        CommentsArticleList,
        UsersList,
        UpdateUser,
        DeleteUser,
        Statistics,
        )


app_name = 'account'
urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("articles", ArticlesList.as_view(), name="articles"),
    path("article/create", CreateArticle.as_view(), name="create-article"),
    path("article/update/<int:pk>", UpdateArticle.as_view(), name="update-article"),
    path("article/delete/<int:pk>", DeleteArticle.as_view(), name="delete-article"),
    path("profile/", Profile.as_view(), name="profile"),
    path("allcomments/", AllCommentList.as_view(), name="allcomments"),
    path("mycomments/", MyCommentList.as_view(), name="mycomments"),
    path("comments/update/<int:pk>", UpdateComment.as_view(), name="update-comment"),
    path("comments/delete/<int:pk>", DeleteComment.as_view(), name="delete-comment"),
    path("comments/article/<int:pk>", CommentsArticleList.as_view(), name="comments-article"),
    path("users", UsersList.as_view(), name="users"),
    path("users/update/<int:pk>", UpdateUser.as_view(), name="update-user"),
    path("users/delete/<int:pk>", DeleteUser.as_view(), name="delete-user"),
    path("statistics", Statistics.as_view(), name='statistics')
]
