from django.contrib import admin
from django.utils.html import format_html
from .models import Student, HollandTest, GardnerTest, HollandQuestionnaireResult, GardnerQuestionnaireResult


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'photo_thumbnail',
        'student_id',
        'student_number',
        'first_name',
        'last_name',
        'sex',
        'age_display',
        'level',
        'room',
        'created_at',
        'updated_at'
    )
    
    list_filter = (
        'level',
        'room',
        'sex',
        'created_at',
        'updated_at',
        'date_of_birth'
    )
    
    search_fields = (
        'student_id',
        'student_number',
        'first_name',
        'last_name',
    )
    
    list_per_page = 25
    
    fieldsets = (
        ('Student Identification', {
            'fields': ('student_id', 'student_number')
        }),
        ('Personal Information', {
            'fields': ('photo', 'first_name', 'last_name', 'sex', 'date_of_birth')
        }),
        ('Academic Information', {
            'fields': ('level', 'room')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    def photo_thumbnail(self, obj):
        """Display thumbnail of student photo in admin list"""
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.photo.url
            )
        return "No Photo"
    photo_thumbnail.short_description = 'Photo'
    
    def age_display(self, obj):
        """Display student's age"""
        return f"{obj.age} years old"
    age_display.short_description = 'Age'
    
    # Custom actions for bulk operations
    def make_level_1(self, request, queryset):
        queryset.update(level='1')
        self.message_user(request, f"{queryset.count()} students moved to Level 1.")
    make_level_1.short_description = "Move selected students to Level 1"
    
    def make_level_2(self, request, queryset):
        queryset.update(level='2')
        self.message_user(request, f"{queryset.count()} students moved to Level 2.")
    make_level_2.short_description = "Move selected students to Level 2"
    
    actions = ['make_level_1', 'make_level_2']


@admin.register(HollandTest)
class HollandTestAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'primary_type',
        'secondary_type',
        'realistic_score',
        'investigative_score',
        'artistic_score',
        'social_score',
        'enterprising_score',
        'conventional_score',
        'test_date'
    )
    
    list_filter = (
        'primary_type',
        'secondary_type',
        'test_date',
    )
    
    search_fields = (
        'student__first_name',
        'student__last_name',
        'student__student_id',
    )
    
    readonly_fields = ('test_date',)


@admin.register(GardnerTest)
class GardnerTestAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'primary_intelligence',
        'secondary_intelligence',
        'linguistic_score',
        'logical_score',
        'spatial_score',
        'musical_score',
        'bodily_score',
        'interpersonal_score',
        'intrapersonal_score',
        'naturalist_score',
        'test_date'
    )
    
    list_filter = (
        'primary_intelligence',
        'secondary_intelligence',
        'test_date',
    )
    
    search_fields = (
        'student__first_name',
        'student__last_name',
        'student__student_id',
    )
    
    readonly_fields = ('test_date',)


@admin.register(HollandQuestionnaireResult)
class HollandQuestionnaireResultAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'holland_test',
        'response_date',
        'response_summary_display'
    )
    
    list_filter = (
        'response_date',
        'holland_test__primary_type',
    )
    
    search_fields = (
        'student__first_name',
        'student__last_name',
        'student__student_id',
    )
    
    readonly_fields = ('response_date', 'response_summary')
    
    def response_summary_display(self, obj):
        """Display summary of responses"""
        responses = obj.response_summary
        return f"Average: {sum(responses)/len(responses):.1f} (Total: {sum(responses)})"
    response_summary_display.short_description = 'Response Summary'


@admin.register(GardnerQuestionnaireResult)
class GardnerQuestionnaireResultAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'gardner_test',
        'response_date',
        'response_summary_display'
    )
    
    list_filter = (
        'response_date',
        'gardner_test__primary_intelligence',
    )
    
    search_fields = (
        'student__first_name',
        'student__last_name',
        'student__student_id',
    )
    
    readonly_fields = ('response_date', 'response_summary')
    
    def response_summary_display(self, obj):
        """Display summary of responses"""
        responses = obj.response_summary
        return f"Average: {sum(responses)/len(responses):.1f} (Total: {sum(responses)})"
    response_summary_display.short_description = 'Response Summary'
