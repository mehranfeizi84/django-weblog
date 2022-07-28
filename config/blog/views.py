from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, TemplateView
from account.models import User
from .models import Article, Category
from account.mixins import AuthorAccessMixin2
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Count, Q


class ArticleList(ListView):
    queryset = Article.objects.published()
    template_name = "blog/home.html"
    context_object_name = "articles"
    paginate_by = 7


def error_404(request, exception):
    return render(request, 'blog/404.html')


class ArticleDetail(DetailView):
    template_name = "blog/post.html"
    context_object_name = "article"

    # get published articles from models
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)

        ip_address = self.request.user.ip_address
        if ip_address not in article.views.all():
            article.views.add(ip_address)

        return article

        
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # send category with context
            article = get_object_or_404(Article, slug=self.kwargs['slug'])
            total_likes = article.total_likes()
            total_dislikes = article.total_dislikes()
            liked = False
            if article.likes.filter(pk=self.request.user.pk).exists():
                liked = True

            disliked = False
            if article.dislikes.filter(pk=self.request.user.pk).exists():
                disliked = True

            context['total_likes'] = total_likes
            context['total_dislikes'] = total_dislikes
            context['liked'] = liked
            context['disliked'] = disliked

            return context

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
        slug = self.kwargs.get('slug')
        global category
        category = get_object_or_404(Category.objects.actived(), slug=slug)
        if slug in ['archive-2022','archive-2021', 'archive-2020']:
            year = 0
            if slug == 'archive-2022':
                year = 2022
            if slug == 'archive-2021':
                year = 2021
            if slug == 'archive-2020':
                year = 2020

            articles = Article.objects.published().filter(Q(publish__year=year))
            return articles

        else:
            # get articles from that category
            articles_category = category.articles.published()

            return articles_category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # send category with context
        context['category'] = category

        return context

    paginate_by = 5

    
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


def LikeView(request, slug):
    article = get_object_or_404(Article, slug=slug)
    liked = False
    if article.likes.filter(pk=request.user.pk).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        article.dislikes.remove(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blog:detail',args=[str(slug)]))


def DislikeView(request, slug):
    article = get_object_or_404(Article, slug=slug)
    disliked = False
    if article.dislikes.filter(pk=request.user.pk).exists():
        article.dislikes.remove(request.user)
        disliked = False
    else:
        article.dislikes.add(request.user)
        article.likes.remove(request.user)
        disliked = True
    return HttpResponseRedirect(reverse('blog:detail',args=[str(slug)]))


class BestArticlesView(TemplateView):
    template_name = "blog/best.html"