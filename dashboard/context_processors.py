from dashboard.models import Application


def pending_applications(request):
    if request.user.is_authenticated:
        try:
            count = Application.objects.filter(status='pending').count()
            return {'pending_count': count}
        except Exception:
            return {'pending_count': 0}
    return {'pending_count': 0}
