from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CommentInLine(admin.TabularInline):
    model = Comment


class ReviewInLine(admin.TabularInline):
    model = Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'display_genre',
        'category',
    )
    search_fields = ('name', )
    list_filter = ('year', 'genre', 'category')
    fields = ['name', ('category', 'genre'), 'year', 'description']
    empty_value_display = '-пусто-'
    inlines = (ReviewInLine,)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'author', 'review')
    list_filter = ('pub_date', 'author', 'review')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    inlines = (CommentInLine,)
    list_display = ('pub_date', 'author', 'title', 'score',)
    list_filter = ('author', 'title', 'score',)
