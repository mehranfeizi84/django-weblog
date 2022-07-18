from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article


# mixin for show cutom fields
class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = [
                "title",
                "slug",
                "category",
                "description",
                "thumbnail",
                "publish",
                "status",
                'is_special',
            ]
        if request.user.is_superuser:
            self.fields.append("author")
        return super().dispatch(request, *args, **kwargs)


# limited choice status for authors and unlimited choice status for superusers
class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'
        return super().form_valid(form)


# get article if you're author and status be back or draft or superuser
class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.status in ['b', 'd'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404(":)مالیدی")


# get article if you're author and status be back or draft or investigation or you're superuser and status be back or draft or investigation
class AuthorAccessMixin2():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.status in ['b', 'i', 'd'] or request.user.is_superuser and article.status in ['d', 'i', 'b']:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404(":)مالیدی")


# if you're not authenticate redirect to login or if you're normal redirect to profile view
class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('account:profile')
        else:
            return redirect('login')


# if you're author that article or you're superuser and article status = draft you have permision to that 
class SuperUserAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if request.user.is_superuser or article.author == request.user\
             and article.status == 'd':
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404(":)مالیدی")
