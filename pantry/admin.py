from django.contrib import admin
from .models import Item, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'quantity',
                    'available', 'created_date', 'updated_date']
    list_filter = ['available', 'created_date', 'updated_date']
    list_editable = ['available']
