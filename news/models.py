from django.db import models
from django.contrib.auth.models import User

news = 'NW'
article = 'AR'
select = 'SL'

POST_TYPE = [
    (news, 'Новость'),
    (article, 'Статья'),
    (select, 'Выбрать')
]


class Author(models.Model):
    rating = models.IntegerField(default=0)
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        posts = Post.objects.filter(author=self.id)
        posts_rating = 0
        comments_posts_rating = 0
        comment_author_rating = 0

        for post in posts:
            posts_rating += post.rating * 3
            for comments in Comment.objects.filter(post=post):
                comments_posts_rating += comments.rating

        for comments in Comment.objects.filter(user=self.id):
            comment_author_rating += comments.rating

        self.rating = posts_rating + comments_posts_rating + comment_author_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    post_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2,
                                 choices=POST_TYPE,
                                 default=select)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview = self.text[:123] + '...'
        return preview


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


# Create your models here.
