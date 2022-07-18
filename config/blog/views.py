from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from account.models import User
from .models import Article, Category
from account.mixins import AuthorAccessMixin2


class ArticleList(ListView):
    queryset = Article.objects.published()
    template_name = "blog/home.html"
    context_object_name = "articles"
    paginate_by = 3


class ArticleDetail(DetailView):
    template_name = "blog/post.html"
    context_object_name = "article"

    # get published articles from models
    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Article.objects.published(), slug=slug)
        return obj


class ArticlePreview(AuthorAccessMixin2, DetailView):
    template_name = "blog/post.html"
    context_object_name = "article"

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Article, pk=pk)
        return obj


class CategoryList(ListView):
    template_name = "blog/category.html"
    context_object_name = "articles"

    # get active category
    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.actived(), slug=slug)
        # get articles from that category
        articles_category = category.articles.published()

        return articles_category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # send category with context
        context['category'] = category

        return context

    paginate_by = 2

    
class AuthorList(ListView):
    template_name = "blog/author.html"
    context_object_name = "articles"

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        # get articles from that user
        articles_author = author.articles.published()

        return articles_author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author

        return context

    paginate_by = 2