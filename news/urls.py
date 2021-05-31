from django.urls import path
from .views import NewsList, NewsDetail, SearchNewsList, NewsCreate, NewsDelete, NewsUpdate, SubscribeView

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', SearchNewsList.as_view()),
    path('add/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('subscribe/<int:pk>', SubscribeView, name='subscribe'),
]