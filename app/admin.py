from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Teacher, Profile

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_teacher')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Profile)