from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/enroll/', views.student_enroll, name='student_enroll'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    
    # Teacher Admin Interface
    path('teacher-admin/', views.teacher_admin, name='teacher_admin'),
    path('teacher-admin/toggle-status/<int:pk>/', views.toggle_student_status, name='toggle_student_status'),
    path('teacher-admin/reset-password/<int:pk>/', views.reset_student_password, name='reset_student_password'),
    path('teacher-admin/delete/<int:pk>/', views.delete_student, name='delete_student'),
    
    # Personality Tests
    path('students/<int:pk>/personality/', views.student_personality, name='student_personality'),
    path('students/<int:pk>/holland-questionnaire/', views.holland_questionnaire, name='holland_questionnaire'),
    path('students/<int:pk>/submit-holland-questionnaire/', views.submit_holland_questionnaire, name='submit_holland_questionnaire'),
    path('students/<int:pk>/ss-career-discovery/', views.ss_career_discovery, name='ss_career_discovery'),
    path('students/<int:pk>/submit-ss-career-discovery/', views.submit_ss_career_discovery, name='submit_ss_career_discovery'),
]
