from django.contrib import admin
from .models import Article, Tag, Review, Like


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at', 'is_confirmed']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['article', 'author', 'rating', 'created_at', 'is_reply']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'article']