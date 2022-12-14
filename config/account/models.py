from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from extension.utils import jalali_converter


# add custom fields to our user class
class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    is_author = models.BooleanField(
        default=False, verbose_name='وضعیت نویسندگی')
    special_user = models.DateTimeField(
        default=timezone.now, verbose_name='کاربر ویژه تا')
    image = models.ImageField(upload_to="avatar",default='image/16410.jpg', verbose_name='آواتار')
    blocked = models.BooleanField(default=False,verbose_name='بلاک شده')

    def jpublish_special(self):
        return jalali_converter(self.special_user)
    jpublish_special.short_description = 'تاریخ اتمام اشتراک'

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False
    is_special_user.boolean = True
    is_special_user.short_description = 'وضعیت کاربر ویژه'
