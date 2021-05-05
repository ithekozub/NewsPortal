import django_filters
from django_filters import FilterSet
from .models import Post, Author
from django.forms import DateInput


class PostsFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок содежит')
    post_time_gt = django_filters.DateTimeFilter(field_name='post_time', widget=DateInput(attrs={'type': 'date'}), label='Дата публикации после', lookup_expr='gt')
    author = django_filters.CharFilter(field_name='author__author__username', lookup_expr='icontains', label='Автор')

    class Meta:
        model = Post
        fields = {
            'author__author__username': [],
        }