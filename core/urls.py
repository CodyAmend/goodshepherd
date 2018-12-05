from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views
from .employees import gs, administrator, volunteer

app_name = 'core'
urlpatterns = [
    path('', TemplateView.as_view(template_name='core.html'), name='core'),
    path('about_us/', views.about_us, name='about_us'),
    path('accounts/signup/', gs.SignUpView.as_view(), name='signup'),
    path('accounts/signup/administrator/', administrator.AdministratorSignUpView.as_view(), name='administrator_signup'),
    path('accounts/signup/volunteer/', volunteer.VolunteerSignUpView.as_view(), name='volunteer_signup'),
    #Volunteer
    path('volunteer_list', views.volunteer_list, name='volunteer_list'),
    path('volunteer/create/', views.volunteer_add, name='volunteer_add'),
    path('volunteer/profile/', views.volunteer_profile_edit, name='volunteer_profile_edit'),
    path('volunteer/<int:pk>/edit/', views.volunteer_edit, name='volunteer_edit'),
    path('volunteer/<int:pk>/delete/', views.volunteer_delete, name='volunteer_delete'),
    #Administrator
    path('administrator_list', views.administrator_list, name='administrator_list'),
    path('administrator/create/', views.administrator_add, name='administrator_add'),
    path('administrator/profile/', views.administrator_profile_edit, name='administrator_profile_edit'),
    path('administrator/<int:pk>/edit/', views.administrator_edit, name='administrator_edit'),
    path('administrator/<int:pk>/delete/', views.administrator_delete, name='administrator_delete'),
]