from django.contrib import admin
from .models import Products, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category','created_at',)
    search_fields = ('category', 'title', 'content',)
    list_filter = ('created_at',)
