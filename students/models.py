from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os
import uuid


def student_photo_upload_path(instance, filename):
    """Generate upload path for student photos"""
    ext = filename.split('.')[-1]
    filename = f'{instance.first_name}_{instance.last_name}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.{ext}'
    return os.path.join('student_photos', filename)


class Student(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    LEVEL_CHOICES = [
        ('1', 'Level 1'),
        ('2', 'Level 2'),
        ('3', 'Level 3'),
        ('4', 'Level 4'),
        ('5', 'Level 5'),
        ('6', 'Level 6'),
    ]
    
    ROOM_CHOICES = [
        ('1', 'Room 1'),
        ('2', 'Room 2'),
        ('3', 'Room 3'),
        ('4', 'Room 4'),
        ('5', 'Room 5'),
        ('6', 'Room 6'),
    ]
    
    # Student Identification (keeping default auto-increment ID)
    student_id = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True,
        help_text="Unique student ID (e.g., STD001, STD002)"
    )
    student_number = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True,
        help_text="Student number for enrollment (e.g., 2024001, 2024002)"
    )
    
    # Personal Information
    photo = models.ImageField(
        upload_to=student_photo_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        help_text="Upload student photo (JPG, JPEG, PNG only)",
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=50, help_text="Student's first name")
    last_name = models.CharField(max_length=50, help_text="Student's last name")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, help_text="Student's gender")
    date_of_birth = models.DateField(help_text="Student's date of birth")
    
    # Academic Information
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, help_text="Student's academic level")
    room = models.CharField(max_length=2, choices=ROOM_CHOICES, help_text="Student's assigned room")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - Level {self.level}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate student's age"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class HollandTest(models.Model):
    """Dr. John L Holland Career Interest Test Results"""
    INTEREST_CHOICES = [
        ('R', 'Realistic (นักสำรวจ)'),
        ('I', 'Investigative (นักวิจัย)'),
        ('A', 'Artistic (นักสร้างสรรค์)'),
        ('S', 'Social (นักสังคม)'),
        ('E', 'Enterprising (นักผจญภัย)'),
        ('C', 'Conventional (นักระบบ)'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='holland_tests')
    
    # Holland RIASEC Scores (0-100)
    realistic_score = models.IntegerField(default=0, help_text="นักสำรวจ - ชอบงานที่ใช้มือ เครื่องมือ")
    investigative_score = models.IntegerField(default=0, help_text="นักวิจัย - ชอบคิด วิเคราะห์ แก้ปัญหา")
    artistic_score = models.IntegerField(default=0, help_text="นักสร้างสรรค์ - ชอบสร้างสรรค์ ศิลปะ")
    social_score = models.IntegerField(default=0, help_text="นักสังคม - ชอบช่วยเหลือคน สอน")
    enterprising_score = models.IntegerField(default=0, help_text="นักผจญภัย - ชอบนำ จัดการ ขาย")
    conventional_score = models.IntegerField(default=0, help_text="นักระบบ - ชอบความเป็นระเบียบ")
    
    primary_type = models.CharField(max_length=1, choices=INTEREST_CHOICES)
    secondary_type = models.CharField(max_length=1, choices=INTEREST_CHOICES, blank=True)
    
    test_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-test_date']
    
    def __str__(self):
        return f"{self.student.full_name} - Holland Test ({self.test_date.strftime('%Y-%m-%d')})"
    
    @property
    def highest_score_type(self):
        scores = {
            'R': self.realistic_score,
            'I': self.investigative_score,
            'A': self.artistic_score,
            'S': self.social_score,
            'E': self.enterprising_score,
            'C': self.conventional_score,
        }
        return max(scores, key=scores.get)
    
    @property
    def holland_code(self):
        scores = {
            'R': self.realistic_score,
            'I': self.investigative_score,
            'A': self.artistic_score,
            'S': self.social_score,
            'E': self.enterprising_score,
            'C': self.conventional_score,
        }
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ''.join([item[0] for item in sorted_scores[:3]])


class GardnerTest(models.Model):
    """Dr. Howard Gardner Multiple Intelligence Test Results"""
    INTELLIGENCE_CHOICES = [
        ('linguistic', 'ภาษาศาสตร์ (Linguistic)'),
        ('logical', 'คณิตศาสตร์-ตรรกะ (Logical-Mathematical)'),
        ('spatial', 'มิติสัมพันธ์ (Spatial)'),
        ('musical', 'ดนตรี (Musical)'),
        ('bodily', 'กายเคลื่อนไหว (Bodily-Kinesthetic)'),
        ('interpersonal', 'มนุษยสัมพันธ์ (Interpersonal)'),
        ('intrapersonal', 'เข้าใจตนเอง (Intrapersonal)'),
        ('naturalist', 'ธรรมชาติวิทยา (Naturalist)'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='gardner_tests')
    
    # Gardner Multiple Intelligence Scores (0-100)
    linguistic_score = models.IntegerField(default=0, help_text="ความสามารถด้านภาษา")
    logical_score = models.IntegerField(default=0, help_text="ความสามารถด้านคณิตศาสตร์-ตรรกะ")
    spatial_score = models.IntegerField(default=0, help_text="ความสามารถด้านมิติสัมพันธ์")
    musical_score = models.IntegerField(default=0, help_text="ความสามารถด้านดนตรี")
    bodily_score = models.IntegerField(default=0, help_text="ความสามารถด้านกายเคลื่อนไหว")
    interpersonal_score = models.IntegerField(default=0, help_text="ความสามารถด้านมนุษยสัมพันธ์")
    intrapersonal_score = models.IntegerField(default=0, help_text="ความสามารถด้านเข้าใจตนเอง")
    naturalist_score = models.IntegerField(default=0, help_text="ความสามารถด้านธรรมชาติวิทยา")
    
    primary_intelligence = models.CharField(max_length=20, choices=INTELLIGENCE_CHOICES)
    secondary_intelligence = models.CharField(max_length=20, choices=INTELLIGENCE_CHOICES, blank=True)
    
    test_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-test_date']
    
    def __str__(self):
        return f"{self.student.full_name} - Gardner Test ({self.test_date.strftime('%Y-%m-%d')})"
    
    @property
    def highest_intelligence(self):
        scores = {
            'linguistic': self.linguistic_score,
            'logical': self.logical_score,
            'spatial': self.spatial_score,
            'musical': self.musical_score,
            'bodily': self.bodily_score,
            'interpersonal': self.interpersonal_score,
            'intrapersonal': self.intrapersonal_score,
            'naturalist': self.naturalist_score,
        }
        return max(scores, key=scores.get)
    
    @property
    def intelligence_profile(self):
        return {
            'linguistic': self.linguistic_score,
            'logical': self.logical_score,
            'spatial': self.spatial_score,
            'musical': self.musical_score,
            'bodily': self.bodily_score,
            'interpersonal': self.interpersonal_score,
            'intrapersonal': self.intrapersonal_score,
            'naturalist': self.naturalist_score,
        }


class HollandQuestionnaireResult(models.Model):
    """Store individual Holland questionnaire responses"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='holland_questionnaire_results')
    holland_test = models.OneToOneField(HollandTest, on_delete=models.CASCADE, related_name='questionnaire_result', null=True, blank=True)
    
    # Store individual question responses (q1 to q36)
    # Questions 1-6: Realistic (R)
    q1 = models.IntegerField(help_text="งานที่ต้องใช้กำลังกาย")
    q2 = models.IntegerField(help_text="งานซ่อมแซมเครื่องมือต่างๆ")
    q3 = models.IntegerField(help_text="งานก่อสร้าง ช่างไม้")
    q4 = models.IntegerField(help_text="งานเกษตร ปศุสัตว์")
    q5 = models.IntegerField(help_text="งานขับรถ เครื่องจักร")
    q6 = models.IntegerField(help_text="งานกิจกรรมกลางแจ้ง")
    
    # Questions 7-12: Investigative (I)
    q7 = models.IntegerField(help_text="งานวิจัย ทดลอง")
    q8 = models.IntegerField(help_text="งานแก้ปัญหาทางคณิตศาสตร์")
    q9 = models.IntegerField(help_text="งานวิเคราะห์ข้อมูล")
    q10 = models.IntegerField(help_text="งานวิทยาศาสตร์")
    q11 = models.IntegerField(help_text="งานสืบสวนสอบสวน")
    q12 = models.IntegerField(help_text="งานพัฒนาเทคโนโลยี")
    
    # Questions 13-18: Artistic (A)
    q13 = models.IntegerField(help_text="งานศิลปะ การวาดภาพ")
    q14 = models.IntegerField(help_text="งานดนตรี การแสดง")
    q15 = models.IntegerField(help_text="งานเขียน วรรณกรรม")
    q16 = models.IntegerField(help_text="งานออกแบบ ตกแต่ง")
    q17 = models.IntegerField(help_text="งานสร้างสรรค์ใหม่ๆ")
    q18 = models.IntegerField(help_text="งานถ่ายภาพ วีดีโอ")
    
    # Questions 19-24: Social (S)
    q19 = models.IntegerField(help_text="งานสอน อบรม")
    q20 = models.IntegerField(help_text="งานให้คำปรึกษา")
    q21 = models.IntegerField(help_text="งานช่วยเหลือผู้อื่น")
    q22 = models.IntegerField(help_text="งานทำงานกับเด็ก")
    q23 = models.IntegerField(help_text="งานดูแลสุขภาพ")
    q24 = models.IntegerField(help_text="งานบริการสังคม")
    
    # Questions 25-30: Enterprising (E)
    q25 = models.IntegerField(help_text="งานขาย การตลาด")
    q26 = models.IntegerField(help_text="งานบริหารจัดการ")
    q27 = models.IntegerField(help_text="งานนำทีม")
    q28 = models.IntegerField(help_text="งานเจรจาต่อรอง")
    q29 = models.IntegerField(help_text="งานธุรกิจ")
    q30 = models.IntegerField(help_text="งานนักการเมือง")
    
    # Questions 31-36: Conventional (C)
    q31 = models.IntegerField(help_text="งานบัญชี การเงิน")
    q32 = models.IntegerField(help_text="งานเลขานุการ")
    q33 = models.IntegerField(help_text="งานธุรการ สำนักงาน")
    q34 = models.IntegerField(help_text="งานจัดระเบียบข้อมูล")
    q35 = models.IntegerField(help_text="งานตรวจสอบ ควบคุม")
    q36 = models.IntegerField(help_text="งานทำรายงานสถิติ")
    
    response_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-response_date']
        verbose_name = 'Holland Questionnaire Result'
        verbose_name_plural = 'Holland Questionnaire Results'
    
    def __str__(self):
        return f"{self.student.full_name} - Holland Questionnaire ({self.response_date.strftime('%Y-%m-%d')})"
    
    def get_responses_by_type(self):
        """Get responses grouped by Holland type"""
        return {
            'R': [self.q1, self.q2, self.q3, self.q4, self.q5, self.q6],
            'I': [self.q7, self.q8, self.q9, self.q10, self.q11, self.q12],
            'A': [self.q13, self.q14, self.q15, self.q16, self.q17, self.q18],
            'S': [self.q19, self.q20, self.q21, self.q22, self.q23, self.q24],
            'E': [self.q25, self.q26, self.q27, self.q28, self.q29, self.q30],
            'C': [self.q31, self.q32, self.q33, self.q34, self.q35, self.q36]
        }
    
    @property
    def response_summary(self):
        """Get summary of all responses"""
        responses = []
        for i in range(1, 37):
            responses.append(getattr(self, f'q{i}'))
        return responses


class GardnerQuestionnaireResult(models.Model):
    """Store individual Gardner questionnaire responses"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='gardner_questionnaire_results')
    gardner_test = models.OneToOneField(GardnerTest, on_delete=models.CASCADE, related_name='questionnaire_result', null=True, blank=True)
    
    # Store individual question responses (q1 to q24)
    # Questions 1-3: Linguistic Intelligence
    q1 = models.IntegerField(help_text="ชอบอ่านหนังสือ และสามารถเล่าเรื่องที่อ่านให้คนอื่นฟังได้ดี")
    q2 = models.IntegerField(help_text="สนุกกับการเล่นคำ เช่น ต่อคำกลอน, คำผวน, หรือปริศนาอักษรไขว้")
    q3 = models.IntegerField(help_text="สามารถเขียนอธิบายความคิดหรือเรื่องราวต่างๆ ได้อย่างชัดเจน")
    
    # Questions 4-6: Logical-Mathematical Intelligence
    q4 = models.IntegerField(help_text="ชอบทำงานกับตัวเลข และสนุกกับการแก้โจทย์ปัญหาคณิตศาสตร์")
    q5 = models.IntegerField(help_text="มักจะมองหาเหตุผลและความเชื่อมโยงของสิ่งต่างๆ รอบตัว")
    q6 = models.IntegerField(help_text="ชอบวางแผนสิ่งต่างๆ อย่างเป็นขั้นเป็นตอน")
    
    # Questions 7-9: Spatial Intelligence
    q7 = models.IntegerField(help_text="สามารถจินตนาการภาพในหัวและมองเห็นเป็นภาพสามมิติได้")
    q8 = models.IntegerField(help_text="มีความสามารถในการอ่านแผนที่หรือจดจำเส้นทางได้ดี")
    q9 = models.IntegerField(help_text="ชอบวาดรูป, ออกแบบ, หรือจัดวางสิ่งของให้สวยงาม")
    
    # Questions 10-12: Bodily-Kinesthetic Intelligence
    q10 = models.IntegerField(help_text="เรียนรู้ได้ดีที่สุดเมื่อได้ลงมือทำด้วยตัวเอง")
    q11 = models.IntegerField(help_text="ชอบเล่นกีฬาหรือทำกิจกรรมที่ต้องเคลื่อนไหวร่างกาย")
    q12 = models.IntegerField(help_text="มีความสามารถในการใช้มือประดิษฐ์หรือซ่อมแซมสิ่งของ")
    
    # Questions 13-15: Musical Intelligence
    q13 = models.IntegerField(help_text="สามารถจดจำทำนองเพลงได้ง่ายและรวดเร็ว")
    q14 = models.IntegerField(help_text="ชอบร้องเพลง, เล่นดนตรี, หรือฟังเพลงเป็นประจำ")
    q15 = models.IntegerField(help_text="มักจะรู้สึกถึงจังหวะและเสียงต่างๆ รอบตัวได้ดี")
    
    # Questions 16-18: Interpersonal Intelligence
    q16 = models.IntegerField(help_text="ชอบทำงานร่วมกับผู้อื่นและเป็นส่วนหนึ่งของทีม")
    q17 = models.IntegerField(help_text="สามารถเข้าใจความรู้สึกและมุมมองของคนอื่นได้ดี")
    q18 = models.IntegerField(help_text="เป็นผู้ให้คำปรึกษาที่ดีและเพื่อนๆ มักจะมาขอความช่วยเหลือ")
    
    # Questions 19-21: Intrapersonal Intelligence
    q19 = models.IntegerField(help_text="รู้จักจุดแข็งและจุดอ่อนของตัวเองเป็นอย่างดี")
    q20 = models.IntegerField(help_text="ชอบใช้เวลาอยู่กับตัวเองเพื่อคิดทบทวนเรื่องต่างๆ")
    q21 = models.IntegerField(help_text="มีเป้าหมายในชีวิตที่ชัดเจนและรู้ว่าตัวเองต้องการอะไร")
    
    # Questions 22-24: Naturalist Intelligence
    q22 = models.IntegerField(help_text="ชอบใช้เวลาอยู่กับธรรมชาติ เช่น เดินป่า, ทำสวน, หรือดูแลสัตว์เลี้ยง")
    q23 = models.IntegerField(help_text="สามารถแยกแยะและจดจำชนิดของพืชหรือสัตว์ต่างๆ ได้")
    q24 = models.IntegerField(help_text="สนใจเรื่องสิ่งแวดล้อมและปรากฏการณ์ทางธรรมชาติ")
    
    response_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-response_date']
        verbose_name = 'Gardner Questionnaire Result'
        verbose_name_plural = 'Gardner Questionnaire Results'
    
    def __str__(self):
        return f"{self.student.full_name} - Gardner Questionnaire ({self.response_date.strftime('%Y-%m-%d')})"
    
    def get_responses_by_intelligence(self):
        """Get responses grouped by intelligence type"""
        return {
            'linguistic': [self.q1, self.q2, self.q3],
            'logical': [self.q4, self.q5, self.q6],
            'spatial': [self.q7, self.q8, self.q9],
            'bodily': [self.q10, self.q11, self.q12],
            'musical': [self.q13, self.q14, self.q15],
            'interpersonal': [self.q16, self.q17, self.q18],
            'intrapersonal': [self.q19, self.q20, self.q21],
            'naturalist': [self.q22, self.q23, self.q24]
        }
    
    @property
    def response_summary(self):
        """Get summary of all responses"""
        responses = []
        for i in range(1, 25):
            responses.append(getattr(self, f'q{i}'))
        return responses
