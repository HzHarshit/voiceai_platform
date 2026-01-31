from django.db import models
from tenants.models import Tenant
from accounts.models import User
from campaigns.models import Campaign


class Call(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('initiated', 'Initiated'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='calls')
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='calls')
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    provider_name = models.CharField(max_length=50, default='mock')
    provider_call_id = models.CharField(max_length=100, blank=True, null=True)
    duration = models.PositiveIntegerField(default=0)  # in seconds
    cost = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calls')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Call'
        verbose_name_plural = 'Calls'
        ordering = ['-created_at']

    def __str__(self):
        return f"Call to {self.phone_number} ({self.status})"
