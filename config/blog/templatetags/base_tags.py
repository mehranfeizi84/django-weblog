from django import template
from ..models import Category
from ..models import Article, Category
from django.db.models import Count, Q
from datetime import datetime, timedelta


register = template.Library()

@register.simple_tag
def title(data="ویجی تک"):
    return data


@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    return {
        "category": Category.objects.filter(status=True)
    }


@register.inclusion_tag("blog/partials/top_articles_month.html")
def top_articles_month():
	last_month = datetime.today() - timedelta(days=30)
	return {
		"articles": Article.objects.published().annotate(
			count=Count('views', filter=Q(articlehit__created__gt=last_month))
		).order_by('-count', '-publish')[:3],
	}


@register.inclusion_tag("blog/partials/top_articles_month2.html")
def top_articles_month2():
    last_month = datetime.today() - timedelta(days=30)
    return {
        "top_articles": Article.objects.published().annotate(
        count=Count('views', filter=Q(articlehit__created__gt=last_month))
        ).order_by('-count', '-publish')[:3]
    }


@register.inclusion_tag("blog/partials/top_articles_year.html")
def top_articles_year():
    last_year = datetime.today() - timedelta(days=365)
    return {
        "top_articles": Article.objects.published().annotate(
        count=Count('views', filter=Q(articlehit__created__gt=last_year))
        ).order_by('-count', '-publish')[:3]
    }


@register.inclusion_tag("blog/partials/top_articles_year2.html")
def top_articles_year2():
    last_year = datetime.today() - timedelta(days=365)
    return {
        "top_articles": Article.objects.published().annotate(
        count=Count('views', filter=Q(articlehit__created__gt=last_year))
        ).order_by('-count', '-publish')[:3]
    }