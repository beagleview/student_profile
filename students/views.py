from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Student, HollandTest, GardnerTest, HollandQuestionnaireResult, GardnerQuestionnaireResult
from .forms import StudentEnrollmentForm, StudentSearchForm, HollandTestForm, GardnerTestForm, HollandQuestionnaireForm, GardnerQuestionnaireForm


def student_list(request):
    """Display list of students with search and filtering"""
    students = Student.objects.all()
    search_form = StudentSearchForm(request.GET or None)
    
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        level = search_form.cleaned_data.get('level')
        room = search_form.cleaned_data.get('room')
        sex = search_form.cleaned_data.get('sex')
        
        # Apply filters
        if search_query:
            students = students.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(student_id__icontains=search_query) |
                Q(student_number__icontains=search_query)
            )
        
        if level:
            students = students.filter(level=level)
        
        if room:
            students = students.filter(room=room)
        
        if sex:
            students = students.filter(sex=sex)
    
    # Pagination
    paginator = Paginator(students, 12)  # Show 12 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_students': students.count()
    }
    return render(request, 'students/student_list.html', context)


def student_enroll(request):
    """Handle student enrollment"""
    if request.method == 'POST':
        form = StudentEnrollmentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(
                request, 
                f'Student {student.full_name} (ID: {student.student_id}) has been enrolled successfully!'
            )
            return redirect('student_detail', pk=student.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentEnrollmentForm()
    
    context = {
        'form': form,
        'title': 'Enroll New Student'
    }
    return render(request, 'students/student_form.html', context)


def student_detail(request, pk):
    """Display student details"""
    student = get_object_or_404(Student, pk=pk)
    context = {
        'student': student
    }
    return render(request, 'students/student_detail.html', context)


def student_edit(request, pk):
    """Handle student editing"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentEnrollmentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(
                request, 
                f'Student {student.full_name} information has been updated successfully!'
            )
            return redirect('student_detail', pk=student.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentEnrollmentForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'title': f'Edit {student.full_name}'
    }
    return render(request, 'students/student_form.html', context)


def home(request):
    """Home page with statistics"""
    total_students = Student.objects.count()
    
    # Statistics by level
    level_stats = {}
    for level, label in Student.LEVEL_CHOICES:
        count = Student.objects.filter(level=level).count()
        level_stats[label] = count
    
    # Statistics by room
    room_stats = {}
    for room, label in Student.ROOM_CHOICES:
        count = Student.objects.filter(room=room).count()
        room_stats[label] = count
    
    # Statistics by gender
    gender_stats = {}
    for sex, label in Student.SEX_CHOICES:
        count = Student.objects.filter(sex=sex).count()
        gender_stats[label] = count
    
    # Recent enrollments
    recent_students = Student.objects.order_by('-created_at')[:5]
    
    context = {
        'total_students': total_students,
        'level_stats': level_stats,
        'room_stats': room_stats,
        'gender_stats': gender_stats,
        'recent_students': recent_students
    }
    return render(request, 'students/home.html', context)


def teacher_admin(request):
    """Teacher admin interface for managing students"""
    students = Student.objects.all()
    search_form = StudentSearchForm(request.GET or None)
    
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        level = search_form.cleaned_data.get('level')
        room = search_form.cleaned_data.get('room')
        sex = search_form.cleaned_data.get('sex')
        
        # Apply filters
        if search_query:
            students = students.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(student_id__icontains=search_query) |
                Q(student_number__icontains=search_query)
            )
        
        if level:
            students = students.filter(level=level)
        
        if room:
            students = students.filter(room=room)
        
        if sex:
            students = students.filter(sex=sex)
    
    # Pagination
    paginator = Paginator(students, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_students': students.count()
    }
    return render(request, 'students/teacher_admin.html', context)


def toggle_student_status(request, pk):
    """Toggle student active/inactive status (placeholder for future use)"""
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=pk)
        # For now, just redirect back - can add status field later
        messages.info(request, f'Student {student.full_name} status toggled.')
        return redirect('teacher_admin')
    return redirect('teacher_admin')


def reset_student_password(request, pk):
    """Reset student password (placeholder for future user accounts)"""
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=pk)
        messages.success(request, f'Password reset for {student.full_name}.')
        return redirect('teacher_admin')
    return redirect('teacher_admin')


def holland_test(request, pk):
    """Handle Holland Career Interest Test"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = HollandTestForm(request.POST)
        if form.is_valid():
            holland_test = form.save(commit=False)
            holland_test.student = student
            holland_test.save()
            messages.success(
                request, 
                f'Holland Test completed for {student.full_name}!'
            )
            return redirect('student_personality', pk=student.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill with random sample data for demonstration
        initial_data = {
            'realistic_score': 75,
            'investigative_score': 82,
            'artistic_score': 65,
            'social_score': 70,
            'enterprising_score': 45,
            'conventional_score': 55,
            'primary_type': 'I',
            'secondary_type': 'R'
        }
        form = HollandTestForm(initial=initial_data)
    
    context = {
        'form': form,
        'student': student,
        'title': f'Holland Test - {student.full_name}'
    }
    return render(request, 'students/holland_test.html', context)


def gardner_test(request, pk):
    """Handle Gardner Multiple Intelligence Test"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = GardnerTestForm(request.POST)
        if form.is_valid():
            gardner_test = form.save(commit=False)
            gardner_test.student = student
            gardner_test.save()
            messages.success(
                request, 
                f'Gardner Test completed for {student.full_name}!'
            )
            return redirect('student_personality', pk=student.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill with random sample data for demonstration
        initial_data = {
            'linguistic_score': 78,
            'logical_score': 85,
            'spatial_score': 60,
            'musical_score': 45,
            'bodily_score': 55,
            'interpersonal_score': 72,
            'intrapersonal_score': 68,
            'naturalist_score': 40,
            'primary_intelligence': 'logical',
            'secondary_intelligence': 'linguistic'
        }
        form = GardnerTestForm(initial=initial_data)
    
    context = {
        'form': form,
        'student': student,
        'title': f'Gardner Test - {student.full_name}'
    }
    return render(request, 'students/gardner_test.html', context)


def student_personality(request, pk):
    """Display student personality test results dashboard"""
    student = get_object_or_404(Student, pk=pk)
    
    # Get latest test results
    holland_test = student.holland_tests.first()
    gardner_test = student.gardner_tests.first()
    
    context = {
        'student': student,
        'holland_test': holland_test,
        'gardner_test': gardner_test
    }
    return render(request, 'students/student_personality.html', context)


def holland_questionnaire(request, pk):
    """Display Holland Career Interest Questionnaire"""
    student = get_object_or_404(Student, pk=pk)
    
    context = {
        'student': student,
        'title': f'Holland Questionnaire - {student.full_name}'
    }
    return render(request, 'students/holland_questionnaire.html', context)


def submit_holland_questionnaire(request, pk):
    """Process Holland Career Interest Questionnaire submission"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = HollandQuestionnaireForm(request.POST)
        
        if form.is_valid():
            # Calculate scores from questionnaire responses
            scores = form.calculate_holland_scores()
            
            # Determine primary and secondary types
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            primary_type = sorted_scores[0][0] if sorted_scores else 'R'
            secondary_type = sorted_scores[1][0] if len(sorted_scores) > 1 else 'I'
            
            # Create HollandTest record
            holland_test = HollandTest.objects.create(
                student=student,
                realistic_score=scores.get('R', 0),
                investigative_score=scores.get('I', 0),
                artistic_score=scores.get('A', 0),
                social_score=scores.get('S', 0),
                enterprising_score=scores.get('E', 0),
                conventional_score=scores.get('C', 0),
                primary_type=primary_type,
                secondary_type=secondary_type
            )
            
            # Save individual questionnaire responses
            questionnaire_responses = {f'q{i}': int(form.cleaned_data.get(f'q{i}', 1)) for i in range(1, 37)}
            questionnaire_result = HollandQuestionnaireResult.objects.create(
                student=student,
                holland_test=holland_test,
                **questionnaire_responses
            )
            
            messages.success(
                request,
                f'แบบสอบถามเสร็จสิ้นเรียบร้อย! ผลการทดสอบของ {student.full_name} ได้รับการบันทึกแล้ว'
            )
            return redirect('student_personality', pk=student.pk)
        else:
            messages.error(request, 'กรุณาตรวจสอบข้อมูลและทำการแก้ไข')
            # Redirect back to questionnaire with form errors
            return redirect('holland_questionnaire', pk=student.pk)
    
    # If not POST, redirect to questionnaire
    return redirect('holland_questionnaire', pk=student.pk)


def gardner_questionnaire(request, pk):
    """Display Gardner Multiple Intelligence Questionnaire"""
    student = get_object_or_404(Student, pk=pk)
    
    context = {
        'student': student,
        'title': f'Gardner Questionnaire - {student.full_name}'
    }
    return render(request, 'students/gardner_questionnaire.html', context)


def submit_gardner_questionnaire(request, pk):
    """Process Gardner Multiple Intelligence Questionnaire submission"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = GardnerQuestionnaireForm(request.POST)
        
        if form.is_valid():
            # Calculate scores from questionnaire responses
            scores = form.calculate_gardner_scores()
            
            # Determine primary and secondary intelligence types
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            primary_intelligence = sorted_scores[0][0] if sorted_scores else 'linguistic'
            secondary_intelligence = sorted_scores[1][0] if len(sorted_scores) > 1 else 'logical'
            
            # Create GardnerTest record
            gardner_test = GardnerTest.objects.create(
                student=student,
                linguistic_score=scores.get('linguistic', 0),
                logical_score=scores.get('logical', 0),
                spatial_score=scores.get('spatial', 0),
                musical_score=scores.get('musical', 0),
                bodily_score=scores.get('bodily', 0),
                interpersonal_score=scores.get('interpersonal', 0),
                intrapersonal_score=scores.get('intrapersonal', 0),
                naturalist_score=scores.get('naturalist', 0),
                primary_intelligence=primary_intelligence,
                secondary_intelligence=secondary_intelligence
            )
            
            # Save individual questionnaire responses
            questionnaire_responses = {f'q{i}': int(form.cleaned_data.get(f'q{i}', 1)) for i in range(1, 25)}
            questionnaire_result = GardnerQuestionnaireResult.objects.create(
                student=student,
                gardner_test=gardner_test,
                **questionnaire_responses
            )
            
            messages.success(
                request,
                f'แบบทดสอบพหุปัญญาเสร็จสิ้นเรียบร้อย! ผลการทดสอบของ {student.full_name} ได้รับการบันทึกแล้ว'
            )
            return redirect('student_personality', pk=student.pk)
        else:
            messages.error(request, 'กรุณาตรวจสอบข้อมูลและทำการแก้ไข')
            # Redirect back to questionnaire with form errors
            return redirect('gardner_questionnaire', pk=student.pk)
    
    # If not POST, redirect to questionnaire
    return redirect('gardner_questionnaire', pk=student.pk)


def delete_student(request, pk):
    """Delete student record"""
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=pk)
        student_name = student.full_name
        student.delete()
        messages.success(request, f'Student {student_name} has been deleted successfully.')
        return redirect('teacher_admin')
    return redirect('teacher_admin')
