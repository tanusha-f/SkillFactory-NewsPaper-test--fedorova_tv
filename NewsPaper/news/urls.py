from django.urls import path
from .views import Posts, PostDetail, PostsSearch, PostAdd# PostList,


urlpatterns = [
    # path('', PostList.as_view()),
    path('', Posts.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search', PostsSearch.as_view()),
    path('add', PostAdd.as_view()),
]