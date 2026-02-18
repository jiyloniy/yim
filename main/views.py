from django.shortcuts import render
from django.utils import timezone
from dashboard.models import (
    Laboratory, Program, Event, Project, Partner, News, SiteSetting
)


def landing_page(request):
    settings = SiteSetting.get_settings()
    laboratories = Laboratory.objects.filter(is_active=True)[:6]
    programs = Program.objects.filter(is_active=True)[:6]
    events = Event.objects.filter(is_active=True, date__gte=timezone.now())[:4]
    projects = Project.objects.filter(is_active=True, is_approved=True)[:6]
    partners = Partner.objects.filter(is_active=True)
    news = News.objects.filter(is_published=True)[:3]

    context = {
        'site': settings,
        'laboratories': laboratories,
        'programs': programs,
        'events': events,
        'projects': projects,
        'partners': partners,
        'news': news,
        'stats': {
            'labs': Laboratory.objects.filter(is_active=True).count(),
            'programs': Program.objects.filter(is_active=True).count(),
            'projects': Project.objects.filter(is_active=True, is_approved=True).count(),
        },
    }
    return render(request, 'main/landing.html', context)
