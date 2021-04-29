from django.shortcuts import render
from django.views.generic import ListView, DeleteView

from .models import Post, Category

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


# Create your views here.
