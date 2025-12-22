from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug')
    ordering = ('title',)
