from django import template
from ..models import Category
from ..models import Article, Category
from django.db.models import Count, Q
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.simple_tag
def title(data="ویجی تک"):
    return data


@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    return {
        "category": Category.objects.filter(status=True)
    }


#########################################################################################


@register.inclusion_tag("blog/partials/sidebar.html")
def top_articles_month():
    last_month = datetime.today() - timedelta(days=30)
    return {
        "articles": Article.objects.published().annotate(
            count=Count('views', filter=Q(articlehit__created__gt=last_month))
        ).order_by('-count', '-publish')[:5],
        "title": "پر بازدید ترین مقالات ماه"
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def top_articles_year():
    last_year = datetime.today() - timedelta(days=365)
    return {
        "articles": Article.objects.published().annotate(
            count=Count('views', filter=Q(articlehit__created__gt=last_year))
        ).order_by('-count', '-publish')[:5],
        "title": "پر بازدید ترین مقالات سال"
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def top_articles_anytime():
    return {
        "articles": Article.objects.published().annotate(
            count=Count('views')
        ).order_by('-count', '-publish')[:5],
        "title": "پر بازدید ترین مقالات همه زمان"
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def top_articles_by_like_month():
    last_month = datetime.today() - timedelta(days=30)
    return {
        "articles": Article.objects.published().annotate(
            count=Count('likes', filter=Q(articlelike__created__gt=last_month))
        ).order_by('-count', '-publish')[:5],
        "title": "محبوب ترین مقالات ماه"
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def top_articles_by_dislike_month():
    last_month = datetime.today() - timedelta(days=30)
    return {
        "articles": Article.objects.published().annotate(
            count=Count('dislikes', filter=Q(articledislike__created__gt=last_month))
        ).order_by('-count', '-publish')[:5],
        "title": "غیر محبوب ترین مقالات ماه"
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def top_articles_by_like_year():
    last_year = datetime.today() - timedelta(days=365)
    return {
        "articles": Article.objects.published().annotate(
            count=Count('likes', filter=Q(articlelike__created__gt=last_year))
        ).order_by('-count', '-publish')[:5],
        "title": "محبوب ترین مقالات سال"
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def top_articles_by_like_anytime():
    return {
        "articles": Article.objects.published().annotate(
            count=Count('likes')
        ).order_by('-count', '-publish')[:5],
        "title": "محبوب ترین مقالات هر زمان"
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def top_articles_by_dislike_anytime():
    return {
        "articles": Article.objects.published().annotate(
            count=Count('dislikes')
        ).order_by('-count', '-publish')[:5],
        "title": "غیر محبوب ترین مقالات هر زمان"
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def hot_articles_month():
    content_type_id = ContentType.objects.get(app_label='blog', model='article').id
    last_month = datetime.today() - timedelta(days=30)
    return {
        "articles": Article.objects.published().annotate(
            count=Count('comments', filter=Q(comments__posted__gt=last_month) & Q(comments__content_type_id=content_type_id))
        ).order_by('-count', '-publish')[:5],
        "title": "پر بحث ترین مقالات ماه"
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def hot_articles_anytime():
    content_type_id = ContentType.objects.get(app_label='blog', model='article').id
    return {
        "articles": Article.objects.published().annotate(
            count=Count('comments', filter=Q(comments__content_type_id=content_type_id))
        ).order_by('-count', '-publish')[:5],
        "title": "پر بحث ترین مقالات هر زمان"
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_views_today():
    last_day = datetime.today() - timedelta(days=1)
    return {
        "title": "بازدید های امروز",
        "finall_count":Article.objects.published().filter(
            Q(articlehit__created__gt=last_day)).count()        
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_views_month():
    last_month = datetime.today() - timedelta(days=30)
    return {
        "title": "بازدید های ماه",
        "finall_count":Article.objects.published().filter(
            Q(articlehit__created__gt=last_month)).count()
    }

@register.inclusion_tag("blog/partials/statistics.html")
def all_views_year():
    last_year = datetime.today() - timedelta(days=365)

    return {
        "title": "بازدید های سال",
        "finall_count":Article.objects.published().filter(
            Q(articlehit__created__gt=last_year)).count()
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_views_all_time():
    today = datetime.today()
    return {
        "title": "کل بازدید ها",
        "finall_count":Article.objects.published().filter(Q(articlehit__created__lte=today)).count()
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_like_today():
    last_day = datetime.today() - timedelta(days=1)
    return {
        "title": "لایک های امروز",
        "finall_count":Article.objects.published().filter(
            Q(articlelike__created__gt=last_day)).count()        
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_like_month():
    last_month = datetime.today() - timedelta(days=30)
    return {
        "title": "لایک های ماه",
        "finall_count":Article.objects.published().filter(
            Q(articlelike__created__gt=last_month)).count()
    }

@register.inclusion_tag("blog/partials/statistics.html")
def all_like_year():
    last_year = datetime.today() - timedelta(days=365)

    return {
        "title": "لایک های سال",
        "finall_count":Article.objects.published().filter(
            Q(articlelike__created__gt=last_year)).count()
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_like_all_time():
    today = datetime.today()
    return {
        "title": "کل لایک ها",
        "finall_count":Article.objects.published().filter(Q(articlelike__created__lte=today)).count()
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_comment_today():
    last_day = datetime.today() - timedelta(days=1)
    return {
        "title": "نظر های امروز",
        "finall_count":Article.objects.published().filter(
            Q(comments__posted__gt=last_day)).count()        
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_comment_month():
    last_month = datetime.today() - timedelta(days=30)
    return {
        "title": "نظر های ماه",
        "finall_count":Article.objects.published().filter(
            Q(comments__posted__gt=last_month)).count()
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_comment_year():
    last_year = datetime.today() - timedelta(days=365)

    return {
        "title": "نظر های سال",
        "finall_count":Article.objects.published().filter(
            Q(comments__posted__gt=last_year)).count()
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_comment_all_time():
    today = datetime.today()
    return {
        "title": "کل نظر ها",
        "finall_count":Article.objects.published().filter(Q(comments__posted__lte=today)).count()
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_dislike_today():
    last_day = datetime.today() - timedelta(days=1)
    return {
        "title": "دیس لایک های امروز",
        "finall_count":Article.objects.published().filter(
            Q(articledislike__created__gt=last_day)).count()        
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_dislike_month():
    last_month = datetime.today() - timedelta(days=30)
    return {
        "title": "دیس لایک های ماه",
        "finall_count":Article.objects.published().filter(
            Q(articledislike__created__gt=last_month)).count()
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_dislike_year():
    last_year = datetime.today() - timedelta(days=365)

    return {
        "title": "دیس لایک های سال",
        "finall_count":Article.objects.published().filter(
            Q(articledislike__created__gt=last_year)).count()
    }


@register.inclusion_tag("blog/partials/statistics.html")
def all_dislike_all_time():
    today = datetime.today()
    return {
        "title": "کل دیس لایک ها",
        "finall_count":Article.objects.published().filter(Q(articledislike__created__lte=today)).count()
    }