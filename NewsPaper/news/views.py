from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime
from django.shortcuts import redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from .models import Post, Author, Category, UserCategory
from .filters import PostFilter
from .forms import PostForm#, #SubsForm


class PostsView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-time_in']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['len_sum'] = len(self.get_queryset())

        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, **kwargs):
        pk_id = self.kwargs.get('pk')
        return Post.objects.get(pk=pk_id)

    def subs(self):
        curr_post = self.get_object()
        subs_list = {}
        for a in curr_post.category.values('id'):
            if not Category.objects.filter(pk=a.get('id'), subscrib=self.request.user).exists():
                subs_list[a.get('id')] = Category.objects.get(pk=a.get('id')).name #.append(Category.objects.get(pk=a.get('id')).name)
        return subs_list

    def postcat(self):
        curr_post = self.get_object()
        post_cat = []
        for a in curr_post.category.values('name'):
            post_cat.append(a.get('name'))
        return post_cat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['subs'] = self.subs()
        context['post_cat'] = self.postcat()

        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostsSearchView(ListView):
    model = Post
    template_name = 'posts_search.html'
    context_object_name = 'postss'
    ordering = ['-time_in']
#    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['time_now'] = datetime.utcnow()
        context['len_sum'] = len(Post.objects.all())

        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    template_name = 'post_add.html'
    context_object_name = 'add'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()

        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_initial(self):
        initial = super().get_initial()
        author = Author.objects.get(user=self.request.user)
        initial['author'] = author
        return initial

    def post(self, request, *args, **kwargs):
        # post_new = Post(type=request.POST('type'), author=request.POST('author'), head=request.POST('head'), text=request.POST('text'))
        # post_new.save()
        form = self.form_class(request.POST)
        if form.is_valid():
            post_new = form.save()

        html_content = render_to_string(
            'post_to_send.html',
            {'post_new': post_new,
             'user': User.objects.get(email='tanyatanya2803@gmail.com').username,}
        )

        msg = EmailMultiAlternatives(
            subject=post_new.head,
            body=post_new.head,
            from_email='tanya-fscf@yandex.ru',
            to=['tanyatanya2803@gmail.com'],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponseRedirect('/posts/add')#super().get(request, *args, **kwargs)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    template_name = 'post_add.html'
    context_object_name = 'update'
    form_class = PostForm

    def get_initial(self):
        initial = super().get_initial()
        author = Author.objects.get(user=self.request.user)
        initial['author'] = author
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_object(self, **kwargs):
        pk_id = self.kwargs.get('pk')
        return Post.objects.get(pk=pk_id)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def subs_add(request, **kwargs):
    pk_id = kwargs.get('pk')

    UserCategory.objects.create(user=request.user, category=Category.objects.get(pk=pk_id))
    return redirect(request.META['HTTP_REFERER'])
