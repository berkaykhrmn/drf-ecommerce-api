from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'price', 'stock', 'is_active', 'category')
    list_filter = ('category', 'is_active')
    list_editable = ('price', 'stock', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug')
    ordering = ('-created_at',)