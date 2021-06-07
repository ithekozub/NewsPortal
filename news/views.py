from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post, Category, Author
from .filters import PostsFilter
from .forms import PostForm
from .tasks import mail_new_post


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10


class SearchNewsList(ListView):
    model = Post
    template_name = 'search_news.html'
    context_object_name = 'news'

    def get_context_data(self,**kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostsFilter(self.request.GET,
                                          queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        mypost = get_object_or_404(Post, id=self.kwargs['pk'])
        category = mypost.category
        subscribed = False
        if category.subscribers.filter(id=self.request.user.id).exists():
            subscribed = True
        context['subscribed'] = subscribed
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news_create.html'
    context_object_name = 'news'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        news_day_limit = 3
        author = Author.objects.get(author=self.request.user)

        if len(Post.objects.filter(author=author, post_time__date=datetime.today())) >= news_day_limit:
            return redirect('/news/day_limit')

        else:
            article = form.save()
            mail_new_post.delay(article.pk)
            return super().form_valid(form)




#    def post(self, request, *args, **kwargs):
        #        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST запроса
        #
        #       if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил то сохраняем новый товар
        #           form.save()

#      return super().get(request, *args, **kwargs)





class NewsDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    context_object_name = 'news'
    queryset = Post.objects.all()
    permission_required = ('news.delete_post',)
    success_url = '/news/'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'news_edit.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

@login_required
def SubscribeView(request, pk):
    mypost = get_object_or_404(Post, id=pk)
    category = mypost.category
    if category.subscribers.filter(id=request.user.id).exists():
        category.subscribers.remove(request.user)
    else:
        category.subscribers.add(request.user)
    return HttpResponseRedirect(reverse('news_detail', args=[str(pk)]))
# Create your views here.
