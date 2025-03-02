from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import User, Student, Teacher, Profile, Attendance
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import viewsets
from .models import User, Student, Teacher, Profile,Attendance
from .serializers import UserSerializer, StudentSerializer, TeacherSerializer, ProfileSerializer
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json



def home(request):
    return render(request, 'home.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_student:
            login(request, user)
            return redirect('student_afl')
        else:
            return HttpResponse("Invalid login details")
    return render(request, 'student_login.html')

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_teacher:
            login(request, user)
            return redirect('teacher_afl')
        else:
            return HttpResponse("Invalid login details")
    teachers = Teacher.objects.all()
    return render(request, 'teacher_login.html', {'teachers': teachers})

def student_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")
        try:
            user = User.objects.create_user(username=username, password=password, is_student=True)
            student = Student.objects.create(user=user, student_id=student_id)
            Profile.objects.create(student=student)
            return redirect('home')
        except IntegrityError:
            return HttpResponse("An error occurred while creating the user")
    return render(request, 'student_register.html')

def teacher_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        teacher_id = request.POST.get('teacher_id')
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")
        try:
            user = User.objects.create_user(username=username, password=password, is_teacher=True)
            Teacher.objects.create(user=user, teacher_id=teacher_id)
            return redirect('home')
        except IntegrityError:
            return HttpResponse("An error occurred while creating the user")
    return render(request, 'teacher_register.html')

@login_required
def student_afl(request):
    student = get_object_or_404(Student, user=request.user)
    attendances = Attendance.objects.filter(student=student)
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        attendances = attendances.filter(date__range=[start_date, end_date])
    
    return render(request, 'student_afl.html', {'student': student, 'attendances': attendances})

@login_required
def teacher_afl(request):
    date_filter = request.GET.get('date')
    if date_filter:
        attendances = Attendance.objects.filter(date=date_filter)
    else:
        attendances = Attendance.objects.all()
    
    paginator = Paginator(attendances, 10)  # Show 10 attendances per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    students = Student.objects.all()
    
    return render(request, 'teacher_afl.html', {'attendances': page_obj, 'students': students})

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        date = request.POST.get('date')
        status = request.POST.get('status')
        student = get_object_or_404(Student, student_id=student_id)
        Attendance.objects.create(student=student, date=date, status=status)
        return redirect('teacher_afl')
    return render(request, 'teacher_afl.html')

@login_required
def add_students(request):
    return render(request, 'add_students.html')


        

@login_required
def student_profile(request):
    student = get_object_or_404(Student, user=request.user)
    profile, created = Profile.objects.get_or_create(student=student)
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.save()
        
        profile.phone_number = request.POST.get('phone_number')
        profile.address = request.POST.get('address')
        profile.bio = request.POST.get('bio')
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        
        return redirect('student_afl')
    
    return render(request, 'student_profile.html', {
        'user': request.user,
        'student': student,
        'profile': profile
    })

def view_student_profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'view_student_profiles.html', {'profiles': profiles})

@csrf_exempt
def bulk_upload_students(request):
    if request.method == "POST" and request.FILES.get("student_file"):
        student_file = request.FILES["student_file"]
        try:
            data = json.load(student_file)  # Load JSON data
            
            for student_data in data:  # Loop through student records
                user_data = student_data.get("user", {})  # Extract user data
                
                # Validate required fields
                username = user_data.get("username", "").strip()
                email = user_data.get("email", "").strip()
                student_id = student_data.get("student_id", "").strip()
                
                if not username or not email or not student_id:
                    messages.error(request, f"Missing required fields for {username}. Skipping.")
                    continue
                
                # Create or get the user
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={"email": email}
                )
                
                # Set user role (student)
                user.is_student = user_data.get("is_student", False)
                user.is_teacher = user_data.get("is_teacher", False)
                user.save()

                # Create student record
                Student.objects.get_or_create(user=user, student_id=student_id)

            messages.success(request, "Students uploaded successfully!")

        except json.JSONDecodeError:
            messages.error(request, "Invalid JSON format.")
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")

    return redirect("teacher_afl")

# API CALLING For USer TO get and Post

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer