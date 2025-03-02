from rest_framework import serializers
from .models import User, Student, Teacher, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_student', 'is_teacher']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'student_id']

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user']

class ProfileSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'student', 'phone_number', 'address', 'bio', 'profile_picture']