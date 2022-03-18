from django.urls import path
from .views import PostsView, PostDetailView, PostsSearchView, PostAddView, PostUpdateView, PostDeleteView# PostList,


urlpatterns = [
    # path('', PostList.as_view()),
    path('', PostsView.as_view()),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('search', PostsSearchView.as_view()),
    path('add', PostAddView.as_view()),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]