from django.db import models


class Meeting(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    reason = models.TextField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    preferred_datetime = models.DateTimeField(null=True, blank=True)
    assigned_datetime = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(blank=True)
    signature = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.organization}"
