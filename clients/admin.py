from django.contrib import admin
from .models import Customer, Visit, VisitItems
# Register your models here.

admin.site.register(Customer)

class VisitItemInline(admin.TabularInline):
    model = VisitItems
    raw_id_fields = ['item']

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'client' ,'picked_up', 'created_date', 'updated_date']
    list_filter = ['picked_up', 'created_date', 'updated_date']
    inlines = [VisitItemInline]