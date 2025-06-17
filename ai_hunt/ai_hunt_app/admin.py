from django.contrib import admin
from .models import Category, Hashtag, Type, Tool


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'type', 'is_verified', 'rating',
        'upvote_count', 'trend_count', 'rank_in_category', 'date_added'
    )
    list_filter = ('is_verified', 'category', 'type', 'hashtags')
    search_fields = ('name', 'description', 'url')
    filter_horizontal = ('hashtags',)
    readonly_fields = ('date_added', 'date_updated')
