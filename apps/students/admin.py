# students/admin.py
from django.contrib import admin
from .models import (
    Student, EnrollmentRequirement, ExamInformation,
    TuitionFee, Document, FAQ, SpiritualGuidance
)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'congregation', 'diocese', 'year_joined', 'status']
    list_filter = ['status', 'congregation', 'diocese', 'year_joined']
    search_fields = ['name', 'student_id', 'email', 'congregation', 'diocese']
    list_editable = ['status']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'student_id', 'photo')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Academic Information', {
            'fields': ('congregation', 'diocese', 'year_joined', 'status')
        }),
    )

@admin.register(EnrollmentRequirement)
class EnrollmentRequirementAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_mandatory', 'order']
    list_filter = ['is_mandatory']
    search_fields = ['title', 'description']
    list_editable = ['is_mandatory', 'order']
    ordering = ['order', 'title']

@admin.register(ExamInformation)
class ExamInformationAdmin(admin.ModelAdmin):
    list_display = ['title', 'exam_date', 'exam_time', 'exam_type', 'is_active']
    list_filter = ['exam_type', 'is_active', 'exam_date']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_active']
    date_hierarchy = 'exam_date'
    ordering = ['-exam_date']

@admin.register(TuitionFee)
class TuitionFeeAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'fee_type', 'academic_year', 'due_date', 'is_active']
    list_filter = ['fee_type', 'is_active', 'academic_year']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    ordering = ['fee_type', 'title']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_required', 'file_size_display']
    list_filter = ['category', 'is_required']
    search_fields = ['title', 'description']
    list_editable = ['is_required']
    ordering = ['category', 'title']
    
    def file_size_display(self, obj):
        if obj.file_size:
            if obj.file_size < 1024 * 1024:
                return f"{obj.file_size / 1024:.1f} KB"
            else:
                return f"{obj.file_size / (1024 * 1024):.1f} MB"
        return "Unknown"
    file_size_display.short_description = "File Size"

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_featured', 'order']
    list_filter = ['category', 'is_featured']
    search_fields = ['question', 'answer']
    list_editable = ['is_featured', 'order']
    ordering = ['category', 'order']

@admin.register(SpiritualGuidance)
class SpiritualGuidanceAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_featured', 'created_at']
    list_filter = ['category', 'is_featured', 'created_at']
    search_fields = ['title', 'content', 'author']
    list_editable = ['is_featured']
    date_hierarchy = 'created_at'
    ordering = ['-is_featured', '-created_at']