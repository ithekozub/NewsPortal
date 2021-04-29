from django.contrib import admin
from .models import Category, Post, Author

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)
# Register your models here.
