from django.contrib import admin
from django.urls import path, include
from account.forms import CustomLogin
from account.views import ChangePassword
from account.views import register


urlpatterns = [
    path('admin/', admin.site.urls),
    # include blog app urls to here
    path('', include('blog.urls')),
    # include login,logout,... urls to here
    path('', include('django.contrib.auth.urls')),
    # include account urls to here
    path('account/', include('account.urls')),
    # custom login,logout,changepassword form
    path("login/", CustomLogin.as_view(), name="login"),
    path("register/", register, name="register"),
    path(
        "password_change/", ChangePassword.as_view(), name="password_change"
    ),
    path('comment/', include('comment.urls')),
]
