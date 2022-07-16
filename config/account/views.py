from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .mixins import FieldsMixin, FormValidMixin, AuthorAccessMixin, SuperUserAccessMixin, AuthorsAccessMixin
from blog.models import Article
from .models import User
from .forms import ProfileForm
from django.contrib.auth.views import PasswordChangeView
from .forms import RegisterForm


class HomeAccount(AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'
    context_object_name = "articles"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class CreateArticle(AuthorsAccessMixin, FormValidMixin, FieldsMixin, CreateView):
    model = Article
    template_name = 'registration/article-create-update.html'


class UpdateArticle(AuthorsAccessMixin, FormValidMixin, FieldsMixin, UpdateView):
    model = Article
    template_name = 'registration/article-create-update.html'


class DeleteArticle(SuperUserAccessMixin, DeleteView):
    model = Article
    template_name = 'registration/article-delete.html'
    success_url = reverse_lazy('account:home')


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm

    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })

        return kwargs


class ChangePassword(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')


def register(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect("/")

    register_form = RegisterForm(request.POST or None)

    if register_form.is_valid():
        user_name = register_form.cleaned_data.get('user_name')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password')
        User.objects.create_user(username=user_name,email=email,password=password)
        return redirect("/login")

    context = {
        'form': register_form
    }

    return render(request, 'registration/register.html', context)

