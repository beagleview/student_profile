from django.core.management.base import BaseCommand
from django.utils import timezone
from students.models import Student
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Create sample student data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Number of students to create (default: 20)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Sample data
        first_names = [
            'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'James', 'Emma',
            'William', 'Olivia', 'Alexander', 'Sophia', 'Benjamin', 'Isabella',
            'Lucas', 'Mia', 'Henry', 'Charlotte', 'Sebastian', 'Amelia'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
            'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
            'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin'
        ]
        
        # Clear existing sample data if needed
        if self.confirm_deletion():
            Student.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('Deleted existing student records')
            )
        
        # Create sample students
        students_created = 0
        
        for i in range(count):
            # Generate random student data
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            sex = random.choice(['M', 'F'])
            level = random.choice(['1', '2', '3', '4', '5', '6'])
            room = random.choice(['1', '2', '3', '4', '5', '6'])
            
            # Generate random birth date (6-18 years old)
            years_old = random.randint(6, 18)
            birth_date = date.today() - timedelta(days=years_old*365 + random.randint(0, 364))
            
            try:
                # Generate unique student_id and student_number
                first_part = first_name[:2].upper()
                last_part = last_name[:2].upper()
                student_id = f'STD{first_part}{last_part}{students_created + 1:03d}'
                student_number = f'2024{students_created + 1:03d}'
                
                student = Student.objects.create(
                    student_id=student_id,
                    student_number=student_number,
                    first_name=first_name,
                    last_name=last_name,
                    sex=sex,
                    date_of_birth=birth_date,
                    level=level,
                    room=room
                )
                students_created += 1
                
                if students_created % 5 == 0:  # Progress indicator
                    self.stdout.write(f'Created {students_created} students...')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating student {first_name} {last_name}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {students_created} students')
        )
        
        # Display summary
        self.display_summary()
    
    def confirm_deletion(self):
        """Ask for confirmation before deleting existing data"""
        existing_count = Student.objects.count()
        if existing_count > 0:
            response = input(
                f'This will delete {existing_count} existing students. '
                f'Continue? (y/N): '
            )
            return response.lower() == 'y'
        return True
    
    def display_summary(self):
        """Display a summary of created students"""
        total = Student.objects.count()
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'SUMMARY: {total} total students')
        self.stdout.write('='*50)
        
        # Count by level
        self.stdout.write('Students by Level:')
        for level, label in Student.LEVEL_CHOICES:
            count = Student.objects.filter(level=level).count()
            self.stdout.write(f'  {label}: {count} students')
        
        # Count by room
        self.stdout.write('\nStudents by Room:')
        for room, label in Student.ROOM_CHOICES:
            count = Student.objects.filter(room=room).count()
            self.stdout.write(f'  {label}: {count} students')
        
        # Count by gender
        self.stdout.write('\nStudents by Gender:')
        for sex, label in Student.SEX_CHOICES:
            count = Student.objects.filter(sex=sex).count()
            self.stdout.write(f'  {label}: {count} students')
        
        self.stdout.write('='*50)
        self.stdout.write('You can now log in to the admin at http://127.0.0.1:8000/admin/')
        self.stdout.write('='*50)
