from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Student, HollandTest, GardnerTest, HollandQuestionnaireResult, GardnerQuestionnaireResult
from .forms import StudentEnrollmentForm, StudentSearchForm, HollandQuestionnaireForm, GardnerQuestionnaireForm


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


def ss_career_discovery(request, pk):
    """Display Samsung Career Discovery Assessment"""
    student = get_object_or_404(Student, pk=pk)
    
    context = {
        'student': student,
        'title': f'Samsung Career Discovery - {student.full_name}'
    }
    return render(request, 'students/career_discovery.html', context)


def submit_ss_career_discovery(request, pk):
    """Process Samsung Career Discovery Assessment submission"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        # Create a custom form handler for the 41-question format
        responses = {}
        
        # Collect all 41 responses
        for i in range(1, 42):
            response = request.POST.get(f'q{i}')
            if response is not None:
                responses[f'q{i}'] = int(response)
            else:
                messages.error(request, f'กรุณาตอบคำถามข้อที่ {i}')
                return redirect('ss_career_discovery', pk=student.pk)
        
        # Map questions to intelligence types (updated mapping for 41 questions)
        question_mapping = {
            # Linguistic Intelligence - Questions: 1, 10, 17, 25, 34
            'linguistic': [1, 10, 17, 25, 34],
            # Musical Intelligence - Questions: 2, 11, 20, 30, 40
            'musical': [2, 11, 20, 30, 40],
            # Bodily-Kinesthetic Intelligence - Questions: 3, 9, 26, 27, 31, 37
            'bodily': [3, 9, 26, 27, 31, 37],
            # Interpersonal Intelligence - Questions: 4, 12, 18, 35, 39
            'interpersonal': [4, 12, 18, 35, 39],
            # Logical-Mathematical Intelligence - Questions: 5, 15, 22, 32
            'logical': [5, 15, 22, 32],
            # Naturalist Intelligence - Questions: 6, 13, 16, 23, 38
            'naturalist': [6, 13, 16, 23, 38],
            # Spatial Intelligence - Questions: 7, 19, 24, 29, 33
            'spatial': [7, 19, 24, 29, 33],
            # Intrapersonal Intelligence - Questions: 8, 14, 21, 28, 36, 41
            'intrapersonal': [8, 14, 21, 28, 36, 41]
        }
        
        # Calculate scores for each intelligence type
        scores = {}
        for intelligence, questions in question_mapping.items():
            total_score = 0
            for q_num in questions:
                total_score += responses.get(f'q{q_num}', 0)
            
            # Convert to percentage (max score per question is 3, so max total varies by intelligence)
            max_possible = len(questions) * 3
            percentage_score = round((total_score / max_possible) * 100) if max_possible > 0 else 0
            scores[intelligence] = percentage_score
        
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
        
        # For compatibility with existing GardnerQuestionnaireResult model (24 questions)
        # Map the first 24 responses to match the model fields
        questionnaire_responses = {}
        for i in range(1, 25):
            questionnaire_responses[f'q{i}'] = responses.get(f'q{i}', 0)
        
        questionnaire_result = GardnerQuestionnaireResult.objects.create(
            student=student,
            gardner_test=gardner_test,
            **questionnaire_responses
        )
        
        messages.success(
            request,
            f'Samsung Career Discovery เสร็จสิ้นเรียบร้อย! ผลการทดสอบของ {student.full_name} ได้รับการบันทึกแล้ว'
        )
        return redirect('student_personality', pk=student.pk)
    
    # If not POST, redirect to questionnaire
    return redirect('ss_career_discovery', pk=student.pk)


def delete_student(request, pk):
    """Delete student record"""
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=pk)
        student_name = student.full_name
        student.delete()
        messages.success(request, f'Student {student_name} has been deleted successfully.')
        return redirect('teacher_admin')
    return redirect('teacher_admin')
