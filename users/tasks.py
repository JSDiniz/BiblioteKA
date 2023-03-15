from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from users.models import User

@shared_task
def unblock_users():
    blocked_users = User.objects.filter(is_blocked=True)
    for user in blocked_users:
        if user.blocked_at + timedelta(days=3) <= timezone.now():
            user.is_blocked = False
            user.blocked_at = None
            user.save()