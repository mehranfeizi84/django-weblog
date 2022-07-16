from django.contrib import admin
from django.urls import path, include
from account.forms import CustomLogin
from account.views import ChangePassword
from account.views import register


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),
    path("login/", CustomLogin.as_view(), name="login"),
    path("register/", register, name="register"),
    path(
        "password_change/", ChangePassword.as_view(), name="password_change"
    ),
]
