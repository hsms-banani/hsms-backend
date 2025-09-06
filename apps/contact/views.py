from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact
from .serializers import ContactSerializer

class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        
        # Send email
        send_mail(
            subject=f"New Contact Form Submission from {instance.name}",
            message=f"Name: {instance.name}\nEmail: {instance.email}\nMessage: {instance.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )