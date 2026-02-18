from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    # Dashboard
    path('', views.student_home, name='home'),

    # Profile
    path('profile/', views.student_profile, name='profile'),

    # Programs
    path('programs/', views.program_list, name='program_list'),
    path('programs/<int:pk>/', views.program_detail, name='program_detail'),
    path('programs/<int:pk>/apply/', views.program_apply, name='program_apply'),

    # My Applications
    path('applications/', views.my_applications, name='my_applications'),
    path('applications/<int:pk>/cancel/', views.cancel_application, name='cancel_application'),

    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),

    # Laboratories
    path('laboratories/', views.laboratory_list, name='laboratory_list'),

    # My Projects
    path('projects/', views.my_projects, name='my_projects'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),

    # Certificates
    path('certificates/', views.my_certificates, name='my_certificates'),

    # News
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
]
