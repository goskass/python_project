
from django.urls import path


from .views import NewsList, NewsDetail, NewsSearch, PostCreateView, PostDeleteView, NewsPostUpdateView, \
    ArticlePostUpdateView, subscriptions

urlpatterns = [
    path('news/',NewsList.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', PostCreateView.as_view(), {'post_type': 'news'}, name='create_news'),
    path('article/create/', PostCreateView.as_view(), {'post_type': 'article'}, name='create_article'),
    path('news/<int:pk>/edit/', NewsPostUpdateView.as_view(), name='update_news'),
    path('article/<int:pk>/edit/', ArticlePostUpdateView.as_view(), name='update_article'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_news'),
    path('article/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_article'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]

