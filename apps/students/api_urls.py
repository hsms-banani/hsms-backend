# apps/students/api_urls.py (CREATE THIS FILE)
from django.urls import path
from .views import (
    StudentList, EnrollmentRequirementList,
    ExamInformationList, TuitionFeeList,
    DocumentList, FAQList, SpiritualGuidanceList,
    CongregationList, api_test
)

app_name = 'students_api'

urlpatterns = [
    path('test/', api_test, name='api-test'),
    path('list/', StudentList.as_view(), name='student-list'),
    path('congregations/', CongregationList.as_view(), name='congregations'),
    path('enrollment/', EnrollmentRequirementList.as_view(), name='enrollment'),
    path('exams/', ExamInformationList.as_view(), name='exams'),
    path('tuition/', TuitionFeeList.as_view(), name='tuition'),
    path('documents/', DocumentList.as_view(), name='documents'),
    path('faqs/', FAQList.as_view(), name='faqs'),
    path('spiritual-guidance/', SpiritualGuidanceList.as_view(), name='spiritual'),
]