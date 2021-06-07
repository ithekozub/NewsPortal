from django.urls import path
from .views import NewsList, NewsDetail, SearchNewsList, NewsCreate, NewsDelete, NewsUpdate, SubscribeView
from django.views.generic import TemplateView

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', SearchNewsList.as_view()),
    path('add/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('subscribe/<int:pk>', SubscribeView, name='subscribe'),
    path('day_limit/', TemplateView.as_view(template_name='Post_limit_PerDay.html')),
]