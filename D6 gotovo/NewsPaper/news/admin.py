from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, Subscription

admin.site.register(Author, verbose_name="Автор")
admin.site.register(Category, verbose_name="Категория")
admin.site.register(Post, verbose_name="Новость")
admin.site.register(PostCategory, verbose_name="Категория новости")
admin.site.register(Comment, verbose_name="Комментарий")
admin.site.register(Subscription, verbose_name="Подписки")
