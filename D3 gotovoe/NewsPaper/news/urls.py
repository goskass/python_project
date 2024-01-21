from django.urls import path
from .views import news_list, news_detail,article_list,article_detail

urlpatterns = [
    path('news/', news_list, name='news_list'),
    path('news/<int:pk>/', news_detail, name='news_detail'),
    path('article/', article_list, name='article_list'),
    path('news/<int:pk>/', article_detail, name='article_detail')
]

