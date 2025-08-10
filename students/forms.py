from django import forms
from django.core.exceptions import ValidationError
from .models import Student, HollandTest, GardnerTest
import re


class StudentEnrollmentForm(forms.ModelForm):
    """
    Form for student enrollment with validation and custom widgets
    """
    
    class Meta:
        model = Student
        fields = [
            'student_id', 
            'student_number', 
            'photo', 
            'first_name', 
            'last_name', 
            'sex', 
            'date_of_birth', 
            'level', 
            'room'
        ]
        
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., STD001, STD002',
                'maxlength': 20
            }),
            'student_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., 2024001, 2024002',
                'maxlength': 20
            }),
            'photo': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100',
                'accept': 'image/jpeg,image/jpg,image/png'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Enter first name',
                'maxlength': 50
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Enter last name',
                'maxlength': 50
            }),
            'sex': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500',
                'type': 'date'
            }),
            'level': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500'
            }),
            'room': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500'
            })
        }
        
        labels = {
            'student_id': 'Student ID',
            'student_number': 'Student Number',
            'photo': 'Student Photo',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'sex': 'Gender',
            'date_of_birth': 'Date of Birth',
            'level': 'Academic Level',
            'room': 'Room Assignment'
        }
        
        help_texts = {
            'student_id': 'Unique identifier (letters and numbers, e.g., STD001)',
            'student_number': 'Enrollment number (numbers preferred, e.g., 2024001)',
            'photo': 'Upload JPG, JPEG, or PNG image (optional)',
            'date_of_birth': 'Select the student\'s birth date',
            'level': 'Choose the appropriate academic level',
            'room': 'Assign student to a classroom'
        }

    def clean_student_id(self):
        """Validate student ID format and uniqueness"""
        student_id = self.cleaned_data.get('student_id')
        if student_id:
            # Check format (letters and numbers only)
            if not re.match(r'^[A-Z0-9]+$', student_id.upper()):
                raise ValidationError(
                    'Student ID must contain only letters and numbers (e.g., STD001)'
                )
            
            # Convert to uppercase for consistency
            student_id = student_id.upper()
            
            # Check uniqueness (exclude current instance if editing)
            existing_student = Student.objects.filter(student_id=student_id)
            if self.instance.pk:
                existing_student = existing_student.exclude(pk=self.instance.pk)
            
            if existing_student.exists():
                raise ValidationError(
                    f'Student ID "{student_id}" is already in use. Please choose a different ID.'
                )
        
        return student_id

    def clean_student_number(self):
        """Validate student number format and uniqueness"""
        student_number = self.cleaned_data.get('student_number')
        if student_number:
            # Check format (numbers preferred, but allow letters)
            if not re.match(r'^[A-Z0-9]+$', student_number.upper()):
                raise ValidationError(
                    'Student number must contain only letters and numbers (e.g., 2024001)'
                )
            
            # Check uniqueness (exclude current instance if editing)
            existing_student = Student.objects.filter(student_number=student_number)
            if self.instance.pk:
                existing_student = existing_student.exclude(pk=self.instance.pk)
            
            if existing_student.exists():
                raise ValidationError(
                    f'Student number "{student_number}" is already in use. Please choose a different number.'
                )
        
        return student_number

    def clean_photo(self):
        """Validate uploaded photo"""
        photo = self.cleaned_data.get('photo')
        if photo:
            # Check file size (limit to 5MB)
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError(
                    'Image file too large. Please upload an image smaller than 5MB.'
                )
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
            if photo.content_type not in allowed_types:
                raise ValidationError(
                    'Invalid image format. Please upload JPG, JPEG, or PNG files only.'
                )
        
        return photo

    def clean_first_name(self):
        """Validate and format first name"""
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            # Remove extra whitespace and capitalize
            first_name = first_name.strip().title()
            
            # Check for valid characters (letters, spaces, hyphens, apostrophes)
            if not re.match(r"^[A-Za-z\s\-']+$", first_name):
                raise ValidationError(
                    'First name can only contain letters, spaces, hyphens, and apostrophes.'
                )
        
        return first_name

    def clean_last_name(self):
        """Validate and format last name"""
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            # Remove extra whitespace and capitalize
            last_name = last_name.strip().title()
            
            # Check for valid characters (letters, spaces, hyphens, apostrophes)
            if not re.match(r"^[A-Za-z\s\-']+$", last_name):
                raise ValidationError(
                    'Last name can only contain letters, spaces, hyphens, and apostrophes.'
                )
        
        return last_name

    def clean_date_of_birth(self):
        """Validate date of birth"""
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            from datetime import date, timedelta
            today = date.today()
            
            # Check if date is not in the future
            if date_of_birth > today:
                raise ValidationError(
                    'Date of birth cannot be in the future.'
                )
            
            # Check reasonable age range (3-25 years old)
            min_date = today - timedelta(days=25*365)  # 25 years ago
            max_date = today - timedelta(days=3*365)   # 3 years ago
            
            if date_of_birth < min_date:
                raise ValidationError(
                    'Student seems too old. Please verify the date of birth.'
                )
            
            if date_of_birth > max_date:
                raise ValidationError(
                    'Student seems too young. Please verify the date of birth.'
                )
        
        return date_of_birth


class StudentSearchForm(forms.Form):
    """
    Form for searching students
    """
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Search by name, student ID, or student number...'
        }),
        label='Search Students'
    )
    
    level = forms.ChoiceField(
        choices=[('', 'All Levels')] + Student.LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500'
        }),
        label='Filter by Level'
    )
    
    room = forms.ChoiceField(
        choices=[('', 'All Rooms')] + Student.ROOM_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500'
        }),
        label='Filter by Room'
    )
    
    sex = forms.ChoiceField(
        choices=[('', 'All Genders')] + Student.SEX_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500'
        }),
        label='Filter by Gender'
    )




class HollandQuestionnaireForm(forms.Form):
    """Form for Holland Career Interest Questionnaire with 36 questions"""
    
    # Generate 36 question fields (q1 to q36)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create 36 question fields
        for i in range(1, 37):
            self.fields[f'q{i}'] = forms.ChoiceField(
                choices=[
                    ('1', '1 - ไม่สนใจเลย'),
                    ('2', '2 - สนใจน้อย'), 
                    ('3', '3 - ปานกลาง'),
                    ('4', '4 - สนใจมาก'),
                    ('5', '5 - สนใจมากที่สุด')
                ],
                widget=forms.RadioSelect,
                required=True
            )
    
    def calculate_holland_scores(self):
        """Calculate RIASEC scores from questionnaire responses"""
        # Question mapping to Holland types (1-based indexing)
        question_mapping = {
            # Realistic (R) - Questions 1-6
            'R': [1, 2, 3, 4, 5, 6],
            # Investigative (I) - Questions 7-12  
            'I': [7, 8, 9, 10, 11, 12],
            # Artistic (A) - Questions 13-18
            'A': [13, 14, 15, 16, 17, 18],
            # Social (S) - Questions 19-24
            'S': [19, 20, 21, 22, 23, 24],
            # Enterprising (E) - Questions 25-30
            'E': [25, 26, 27, 28, 29, 30],
            # Conventional (C) - Questions 31-36
            'C': [31, 32, 33, 34, 35, 36]
        }
        
        scores = {}
        for holland_type, questions in question_mapping.items():
            total_score = 0
            for q_num in questions:
                response_value = int(self.cleaned_data.get(f'q{q_num}', 1))
                total_score += response_value
            
            # Convert to percentage (6 questions × 5 max points = 30 max, convert to 100 scale)
            percentage_score = (total_score / 30) * 100
            scores[holland_type] = round(percentage_score)
        
        return scores


class GardnerQuestionnaireForm(forms.Form):
    """Form for Gardner Multiple Intelligence Questionnaire"""
    
    # Generate question fields based on Howard Gardner's Multiple Intelligences
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create question fields for each intelligence type
        # Based on the Howard.html questions but adapted for our system
        questions = [
            # Linguistic (3 questions)
            ('ชอบอ่านหนังสือ และสามารถเล่าเรื่องที่อ่านให้คนอื่นฟังได้ดี', 'linguistic'),
            ('สนุกกับการเล่นคำ เช่น ต่อคำกลอน, คำผวน, หรือปริศนาอักษรไขว้', 'linguistic'),
            ('สามารถเขียนอธิบายความคิดหรือเรื่องราวต่างๆ ได้อย่างชัดเจน', 'linguistic'),
            
            # Logical-Mathematical (3 questions)
            ('ชอบทำงานกับตัวเลข และสนุกกับการแก้โจทย์ปัญหาคณิตศาสตร์', 'logical'),
            ('มักจะมองหาเหตุผลและความเชื่อมโยงของสิ่งต่างๆ รอบตัว', 'logical'),
            ('ชอบวางแผนสิ่งต่างๆ อย่างเป็นขั้นเป็นตอน', 'logical'),
            
            # Spatial (3 questions)
            ('สามารถจินตนาการภาพในหัวและมองเห็นเป็นภาพสามมิติได้', 'spatial'),
            ('มีความสามารถในการอ่านแผนที่หรือจดจำเส้นทางได้ดี', 'spatial'),
            ('ชอบวาดรูป, ออกแบบ, หรือจัดวางสิ่งของให้สวยงาม', 'spatial'),
            
            # Bodily-Kinesthetic (3 questions)
            ('เรียนรู้ได้ดีที่สุดเมื่อได้ลงมือทำด้วยตัวเอง', 'bodily'),
            ('ชอบเล่นกีฬาหรือทำกิจกรรมที่ต้องเคลื่อนไหวร่างกาย', 'bodily'),
            ('มีความสามารถในการใช้มือประดิษฐ์หรือซ่อมแซมสิ่งของ', 'bodily'),
            
            # Musical (3 questions)
            ('สามารถจดจำทำนองเพลงได้ง่ายและรวดเร็ว', 'musical'),
            ('ชอบร้องเพลง, เล่นดนตรี, หรือฟังเพลงเป็นประจำ', 'musical'),
            ('มักจะรู้สึกถึงจังหวะและเสียงต่างๆ รอบตัวได้ดี', 'musical'),
            
            # Interpersonal (3 questions)
            ('ชอบทำงานร่วมกับผู้อื่นและเป็นส่วนหนึ่งของทีม', 'interpersonal'),
            ('สามารถเข้าใจความรู้สึกและมุมมองของคนอื่นได้ดี', 'interpersonal'),
            ('เป็นผู้ให้คำปรึกษาที่ดีและเพื่อนๆ มักจะมาขอความช่วยเหลือ', 'interpersonal'),
            
            # Intrapersonal (3 questions)
            ('รู้จักจุดแข็งและจุดอ่อนของตัวเองเป็นอย่างดี', 'intrapersonal'),
            ('ชอบใช้เวลาอยู่กับตัวเองเพื่อคิดทบทวนเรื่องต่างๆ', 'intrapersonal'),
            ('มีเป้าหมายในชีวิตที่ชัดเจนและรู้ว่าตัวเองต้องการอะไร', 'intrapersonal'),
            
            # Naturalist (3 questions)
            ('ชอบใช้เวลาอยู่กับธรรมชาติ เช่น เดินป่า, ทำสวน, หรือดูแลสัตว์เลี้ยง', 'naturalist'),
            ('สามารถแยกแยะและจดจำชนิดของพืชหรือสัตว์ต่างๆ ได้', 'naturalist'),
            ('สนใจเรื่องสิ่งแวดล้อมและปรากฏการณ์ทางธรรมชาติ', 'naturalist')
        ]
        
        for i, (question_text, intelligence_type) in enumerate(questions, 1):
            self.fields[f'q{i}'] = forms.ChoiceField(
                choices=[
                    ('1', '1 - ไม่เห็นด้วยเลย'),
                    ('2', '2 - เห็นด้วยน้อย'), 
                    ('3', '3 - ปานกลาง'),
                    ('4', '4 - เห็นด้วยมาก'),
                    ('5', '5 - เห็นด้วยมากที่สุด')
                ],
                widget=forms.RadioSelect,
                required=True,
                label=question_text
            )
            # Store intelligence type as field attribute for scoring
            self.fields[f'q{i}'].intelligence_type = intelligence_type
    
    def calculate_gardner_scores(self):
        """Calculate Gardner Multiple Intelligence scores from questionnaire responses"""
        # Intelligence type mapping
        intelligence_types = ['linguistic', 'logical', 'spatial', 'bodily', 'musical', 'interpersonal', 'intrapersonal', 'naturalist']
        
        scores = {intelligence: 0 for intelligence in intelligence_types}
        type_counts = {intelligence: 0 for intelligence in intelligence_types}
        
        # Count questions per intelligence type and calculate scores
        for field_name, field in self.fields.items():
            if field_name.startswith('q') and hasattr(field, 'intelligence_type'):
                intelligence_type = field.intelligence_type
                type_counts[intelligence_type] += 1
                
                if field_name in self.cleaned_data:
                    response_value = int(self.cleaned_data[field_name])
                    scores[intelligence_type] += response_value
        
        # Convert to percentage scores
        percentage_scores = {}
        for intelligence, total_score in scores.items():
            max_possible = type_counts[intelligence] * 5  # 5 is max score per question
            if max_possible > 0:
                percentage_scores[intelligence] = round((total_score / max_possible) * 100)
            else:
                percentage_scores[intelligence] = 0
        
        return percentage_scores


