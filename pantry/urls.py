from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'pantry'
urlpatterns = [
    path('inventory/', views.item_list, name='item_list'),
    path('inventory/<slug:category_slug>/', views.item_list, name='item_list_by_category'),
    path('item/create/', views.item_new, name='item_new'),
    path('item/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),
]