from django.shortcuts import redirect, get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .mixins import (
    FieldsMixin,
    FieldsMixin2,
    FieldsMixin3,
    FieldsMixin4,
    FormValidMixin,
    AuthorAccessMixin,
    SuperUserAccessMixin,
    AuthorsAccessMixin,
    DeleteCommentAccessMixin,
)
from blog.models import Article
from .models import User
from .forms import ProfileForm
from django.contrib.auth.views import PasswordChangeView
from .forms import RegisterForm
from comment.models.comments import Comment
from django.http import HttpResponse
import requests
import json
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime


class Home(AuthorsAccessMixin, TemplateView):
    template_name = 'registration/home.html'


class ArticlesList(AuthorsAccessMixin, ListView):
    template_name = 'registration/articles.html'
    context_object_name = "articles"

    def get_queryset(self):
        # if you're superuser you can see all article in website else you just can see your articles
        if self.request.user.is_superuser:
            global all_article
            all_article = Article.objects.all()
            return all_article
        else:
            global filter_article
            filter_article = Article.objects.filter(author=self.request.user)
            return filter_article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # send category with context
        if self.request.user.is_superuser:
            count = all_article.count()
        else:
            count = filter_article.count()
        context['count'] = count

        return context


class CreateArticle(AuthorsAccessMixin, FormValidMixin, FieldsMixin, CreateView):
    model = Article
    template_name = 'registration/article-create-update.html'


class UpdateArticle(AuthorsAccessMixin, FormValidMixin, FieldsMixin, UpdateView):
    model = Article
    template_name = 'registration/article-create-update.html'


class DeleteArticle(SuperUserAccessMixin, DeleteView):
    model = Article
    template_name = 'registration/article-delete.html'
    # after being operation successful,it redirects to home account
    success_url = reverse_lazy('account:articles')


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    # after being operation successful,it redirects to profile
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        # you receive the users pk and you find the users that has this pk
        return get_object_or_404(User, pk=self.request.user.pk)

    # update the kwargs and send a new kwarg
    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })

        return kwargs


class ChangePassword(PasswordChangeView):
    # after being operation successful,it redirects to password change done view
    success_url = reverse_lazy('password_change_done')


def register(request, *args, **kwargs):
    # if you're authenticate you will redirect to home
    if request.user.is_authenticated:
        return redirect("/")

    # choice custom register form for register operation
    register_form = RegisterForm(request.POST or None)

    if register_form.is_valid():
        user_name = register_form.cleaned_data.get('user_name')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password')
        # get information in form and create a user with that information
        User.objects.create_user(
            username=user_name, email=email, password=password)
        return redirect("/login")

    context = {
        'form': register_form
    }

    return render(request, 'registration/register.html', context)


class AllCommentList(LoginRequiredMixin, ListView):
    template_name = 'registration/commentlist.html'
    context_object_name = "comments"

    def get_queryset(self):
        global comments
        comments = Comment.objects.all()
        return comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # send category with context
        count = comments.count()
        context['count'] = count

        return context


class MyCommentList(LoginRequiredMixin, ListView):
    template_name = 'registration/commentlist.html'
    context_object_name = "comments"

    def get_queryset(self):
        global comments
        comments = Comment.objects.filter(user=self.request.user)
        return comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # send category with context
        count = comments.count()
        context['count'] = count

        return context


class UpdateComment(FieldsMixin2, AuthorsAccessMixin, UpdateView):
    model = Comment
    template_name = 'registration/comments-create-update.html'
    success_url = reverse_lazy('account:allcomments')


class DeleteComment(DeleteCommentAccessMixin, DeleteView):
    model = Comment
    template_name = 'registration/comment-delete.html'
    # after being operation successful,it redirects to home comments
    success_url = reverse_lazy('account:allcomments')


class CommentsArticleList(AuthorsAccessMixin, ListView):
    template_name = 'registration/commentlistarticle.html'
    context_object_name = "comments"

    def get_queryset(self):
        global article
        pk = self.kwargs.get('pk')
        article = Article.objects.get(pk=pk)
        return article.comments.all

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # send category with context
        context['article'] = article

        return context


class UsersList(AuthorsAccessMixin, ListView):
    template_name = 'registration/users.html'
    context_object_name = "users"

    def get_queryset(self):
        global users
        users = User.objects.all()
        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # send category with context
        context['count'] = users.count()

        return context


class UpdateUser(AuthorsAccessMixin, FieldsMixin4, UpdateView):
    model = User
    template_name = 'registration/user-create-update.html'
    success_url = reverse_lazy('account:users')


class DeleteUser(AuthorsAccessMixin, DeleteView):
    model = User
    template_name = 'registration/user-delete.html'
    # after being operation successful,it redirects to home comments
    success_url = reverse_lazy('account:users')


class Statistics(TemplateView):
    template_name = 'registration/statistics.html'


# you should get merchant id from payment
# i used zarinpal for payment
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
CallbackURL = 'http://127.0.0.1:8000/verify/'


@login_required
def send_request(request):
    global amount
    amount = 11000
    description = "description for pay"
    email = request.user.email
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required
def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(
            req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                user = request.user
                user.special_user = datetime.now() + timedelta(days=30)
                user.save()

                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')
