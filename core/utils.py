from .models import User, FriendRequest
from django.utils import timezone


def request_count_limit(user_id):
    time_threshold = timezone.now() - timezone.timedelta(minutes=1)
    recent_requests_count = FriendRequest.objects.filter(
        from_user=user_id, created_at__gte=time_threshold).count()
    if recent_requests_count >= 3:
        return False
    return True
