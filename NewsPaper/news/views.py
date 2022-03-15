from django.views.generic import DetailView, ListView, UpdateView
from datetime import datetime
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class Posts(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-time_in']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['len_sum'] = len(self.get_queryset())
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostsSearch(ListView):
    model = Post
    template_name = 'posts_search.html'
    context_object_name = 'postss'
    ordering = ['-time_in']
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['time_now'] = datetime.utcnow()
        context['len_sum'] = len(Post.objects.all())
        return context


class PostAdd(ListView):
    model = Post
    template_name = 'post_add.html'
    context_object_name = 'post'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


# class PostUpdate(UpdateView):
#     model = Post
#     template_name = 'post_add.html'
#     context_object_name = 'post'
#     form_class = PostForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['time_now'] = datetime.utcnow()
#         context['form'] = PostForm()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()

        return super().get(request, *args, **kwargs)


# class Posts(View):
#     def get(self, request):
#         posts = Post.objects.order_by('-time_in')
#         p = Paginator(posts, 3)
#         posts = p.get_page(request.GET.get('page', 1))
#         data = {
#             'posts': posts,
#         }
#         return render(request, 'posts.html', data)


# class PostList(ListView):
#     model = Post
#     template_name = 'posts.html'
#     context_object_name = 'posts'
#     queryset = Post.objects.order_by('-time_in')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['time_now'] = datetime.utcnow()
#         return context


