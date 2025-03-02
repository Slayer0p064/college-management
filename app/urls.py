from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, StudentViewSet, TeacherViewSet, ProfileViewSet

# API CALLING

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('', include(router.urls)),
    path('student/login/', views.student_login, name='student_login'),
    path('student/register/', views.student_register, name='student_register'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/register/', views.teacher_register, name='teacher_register'),
    path('student/attendance/', views.student_afl, name='student_afl'),
    path('teacher/attendance/', views.teacher_afl, name='teacher_afl'),
    path('teacher/add_students/', views.add_students, name='add_students'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path("bulk-upload-students/", views.bulk_upload_students, name="bulk_upload_students"),
    path('view_student_profiles/', views.view_student_profiles, name='view_student_profiles'),
]