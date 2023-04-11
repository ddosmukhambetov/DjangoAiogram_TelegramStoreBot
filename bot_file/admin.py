from django.contrib import admin
from .models import Product, Category, TelegramUser


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'created_at', 'product_category', 'is_published']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', 'price']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name']


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_login', 'registered_at', 'is_registered']
    list_display_links = ['id', 'user_login']
    search_fields = ['id', 'user_login', 'registered_at']
    readonly_fields = ['user_password', 'is_registered']
