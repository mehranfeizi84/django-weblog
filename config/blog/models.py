from django.db import models
from django.utils.html import format_html
from account.models import User
from django.urls import reverse
import datetime
from extension.utils import jalali_converter
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


class ArticleManger(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManger(models.Manager):
    def actived(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name='children',
                               verbose_name='دسته اصلی')
    title = models.CharField(max_length=200, verbose_name='عنوان دسنه بندی')
    slug = models.SlugField(max_length=100, unique=True,
                            verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='وضعیت')
    position = models.IntegerField(verbose_name='موقعیت')

    objects = CategoryManger()

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیشنویس'),        #draft
        ('p', 'منتشر شده'),      #published
        ('i', 'درحال بررسی'),    #investigation
        ('b', 'برگشت داده شده'), #back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                               related_name='articles', verbose_name='نویسنده')
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=100, unique=True,
                            verbose_name='آدرس مقاله')
    category = models.ManyToManyField(
        Category, verbose_name='دسته بندی', related_name='articles')
    description = models.TextField(verbose_name='توضیحات')
    thumbnail = models.ImageField(upload_to="image", verbose_name='عکس')
    publish = models.DateTimeField(
        default=datetime.datetime.now, verbose_name='تاریخ انتشار')
    created = models.TimeField(auto_now_add=True, verbose_name='زمان ساخت')
    updated = models.TimeField(auto_now=True, verbose_name='زمان آخرین آپدیت')
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')
    comments = GenericRelation(Comment)
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')

    objects = ArticleManger()

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['publish']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    # for redirect to home account
    def get_absolute_url(self):
        return reverse('account:home')

    # to look better date/time publish
    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = 'تاریخ انتشار'

    def publish_category(self):
        return self.category.filter(status=True)

    # show category in panel
    def category_to_str(self):
        return ",".join([category.title for category in self.category.actived()])
    category_to_str.short_description = 'دسته بندی'

    # to show thumbnail article in panel
    def thumbnail_tag(self):
        return format_html("<img height=100 width=120 style='border-radius: 7px;' src='{}'>".format(self.thumbnail.url))
    thumbnail_tag.short_description = 'عکس'
