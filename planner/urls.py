from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'), 
    path('login/', auth_views.LoginView.as_view(template_name='planner/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/add/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:assignment_id>/toggle/', views.toggle_assignment, name='toggle_assignment'),
    path('assignments/<int:assignment_id>/edit/', views.assignment_edit, name='assignment_edit'),
    path('assignments/<int:assignment_id>/delete/', views.assignment_delete, name='assignment_delete'),
    path('courses/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('courses/<int:course_id>/edit/', views.course_edit, name='course_edit'),
]