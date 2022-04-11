from django.urls import path
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    # path('posts/update/<int:pk>', IndexView.as_view()),

]
