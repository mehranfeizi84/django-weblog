from django.urls import path
from blog.views import ArticleDetail, CategoryList, ArticleList, AuthorList, ArticlePreview, LikeView, DislikeView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'
urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
    path('page/<int:page>', ArticleList.as_view(), name='home'),
    path('article/<slug>', ArticleDetail.as_view(), name='detail'),
    path('preview/<pk>', ArticlePreview.as_view(), name='preview'),
    path('category/<slug>', CategoryList.as_view(), name='category'),
    path('category/<slug>/page/<int:page>', CategoryList.as_view(), name='category'),
    path('author/<username>', AuthorList.as_view(), name='author'),
    path('author/<username>/page/<int:page>', AuthorList.as_view(), name='author'),
    path('like/<slug>', LikeView, name='like'),
    path('dislike/<slug>', DislikeView, name='dislike'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)