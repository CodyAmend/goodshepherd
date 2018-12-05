from django.urls import path
from . import views

app_name = 'clients'
urlpatterns = [
   path('client/register/', views.client_form, name='client_form'),
   path('client_list', views.client_list, name='client_list'),
   path('client/<int:pk>/edit/', views.client_edit, name='client_edit'),
   path('client/<int:pk>/delete/', views.client_delete, name='client_delete'),
   path('client/search/', views.client_search, name='client_search'),
   path('client/visit_list', views.visit_list, name='visit_list'),
   path('client/visit/create/', views.visit_create, name='visit_create'),
   path('client/visit/<int:pk>/edit/', views.visit_edit, name='visit_edit'),
   path('client/visit/<int:pk>/delete/', views.visit_delete, name='visit_delete'),
   #path('client/report/', views.generate_report, name='generate_report'),
   path('client/report/csv/', views.generate_report, name='generate_report'),
]