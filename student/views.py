from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from functools import wraps

from accounts.models import User
from dashboard.models import (
    Laboratory, Program, Event, Project,
    Application, Certificate, News, SiteSetting
)
from .forms import (
    StudentLoginForm, StudentRegisterForm, StudentProfileForm,
    ApplicationForm, StudentProjectForm
)


def student_required(view_func):
    @wraps(view_func)
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper


# ==================== AUTH ====================

def student_login(request):
    if request.user.is_authenticated:
        return redirect('student:home')
    form = StudentLoginForm()
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.get_full_name() or user.username}!")
                return redirect('student:home')
            else:
                messages.error(request, "Login yoki parol xato!")
    return render(request, 'student/login.html', {'form': form})


def student_register(request):
    if request.user.is_authenticated:
        return redirect('student:home')
    form = StudentRegisterForm()
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            return redirect('student:home')
    return render(request, 'student/register.html', {'form': form})


def student_logout(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect('login')


# ==================== DASHBOARD ====================

@student_required
def student_home(request):
    my_applications = Application.objects.filter(user=request.user).select_related('program')[:5]
    my_certificates = Certificate.objects.filter(user=request.user)[:5]
    upcoming_events = Event.objects.filter(date__gte=timezone.now(), is_active=True)[:4]
    active_programs = Program.objects.filter(is_active=True)[:4]
    latest_news = News.objects.filter(is_published=True)[:3]
    my_projects = Project.objects.filter(author=request.user, is_active=True)[:3]

    context = {
        'my_applications': my_applications,
        'my_certificates': my_certificates,
        'upcoming_events': upcoming_events,
        'active_programs': active_programs,
        'latest_news': latest_news,
        'my_projects': my_projects,
        'total_applications': Application.objects.filter(user=request.user).count(),
        'approved_applications': Application.objects.filter(user=request.user, status='approved').count(),
        'total_certificates': Certificate.objects.filter(user=request.user).count(),
        'total_projects': Project.objects.filter(author=request.user).count(),
    }
    return render(request, 'student/home.html', context)


# ==================== PROFILE ====================

@student_required
def student_profile(request):
    form = StudentProfileForm(instance=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi!")
            return redirect('student:profile')
    return render(request, 'student/profile.html', {'form': form})


# ==================== PROGRAMS ====================

@student_required
def program_list(request):
    programs = Program.objects.filter(is_active=True)
    level_filter = request.GET.get('level', '')
    format_filter = request.GET.get('format', '')
    search = request.GET.get('search', '')
    lab_filter = request.GET.get('lab', '')

    if level_filter:
        programs = programs.filter(level=level_filter)
    if format_filter:
        programs = programs.filter(format=format_filter)
    if search:
        programs = programs.filter(name__icontains=search)
    if lab_filter:
        programs = programs.filter(laboratory_id=lab_filter)

    labs = Laboratory.objects.filter(is_active=True)
    context = {
        'programs': programs,
        'labs': labs,
        'level_filter': level_filter,
        'format_filter': format_filter,
        'search': search,
        'lab_filter': lab_filter,
    }
    return render(request, 'student/programs/list.html', context)


@student_required
def program_detail(request, pk):
    program = get_object_or_404(Program, pk=pk, is_active=True)
    already_applied = Application.objects.filter(user=request.user, program=program).exists()
    return render(request, 'student/programs/detail.html', {
        'program': program,
        'already_applied': already_applied,
    })


@student_required
def program_apply(request, pk):
    program = get_object_or_404(Program, pk=pk, is_active=True)
    if Application.objects.filter(user=request.user, program=program).exists():
        messages.warning(request, "Siz bu dasturga allaqachon ariza topshirgansiz!")
        return redirect('student:program_detail', pk=pk)

    form = ApplicationForm()
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.program = program
            app.save()
            messages.success(request, "Arizangiz muvaffaqiyatli topshirildi!")
            return redirect('student:my_applications')
    return render(request, 'student/programs/apply.html', {
        'program': program,
        'form': form,
    })


# ==================== APPLICATIONS ====================

@student_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).select_related('program')
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    return render(request, 'student/applications.html', {
        'applications': applications,
        'status_filter': status_filter,
    })


@student_required
def cancel_application(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    if app.status == 'pending':
        app.delete()
        messages.success(request, "Ariza bekor qilindi!")
    else:
        messages.error(request, "Faqat kutilmoqda holatidagi arizalarni bekor qilish mumkin!")
    return redirect('student:my_applications')


# ==================== EVENTS ====================

@student_required
def event_list(request):
    events = Event.objects.filter(is_active=True)
    type_filter = request.GET.get('type', '')
    if type_filter:
        events = events.filter(event_type=type_filter)
    return render(request, 'student/events/list.html', {
        'events': events,
        'type_filter': type_filter,
    })


@student_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    return render(request, 'student/events/detail.html', {'event': event})


# ==================== LABORATORIES ====================

@student_required
def laboratory_list(request):
    labs = Laboratory.objects.filter(is_active=True)
    return render(request, 'student/laboratories.html', {'laboratories': labs})


# ==================== PROJECTS ====================

@student_required
def my_projects(request):
    projects = Project.objects.filter(author=request.user)
    return render(request, 'student/projects/list.html', {'projects': projects})


@student_required
def project_create(request):
    form = StudentProjectForm()
    if request.method == 'POST':
        form = StudentProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            messages.success(request, "Loyiha muvaffaqiyatli qo'shildi!")
            return redirect('student:my_projects')
    return render(request, 'student/projects/form.html', {'form': form})


@student_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    form = StudentProjectForm(instance=project)
    if request.method == 'POST':
        form = StudentProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Loyiha muvaffaqiyatli yangilandi!")
            return redirect('student:my_projects')
    return render(request, 'student/projects/form.html', {'form': form, 'project': project})


# ==================== CERTIFICATES ====================

@student_required
def my_certificates(request):
    certificates = Certificate.objects.filter(user=request.user).select_related('program')
    return render(request, 'student/certificates.html', {'certificates': certificates})


# ==================== NEWS ====================

@student_required
def news_list(request):
    news = News.objects.filter(is_published=True)
    return render(request, 'student/news/list.html', {'news_items': news})


@student_required
def news_detail(request, slug):
    article = get_object_or_404(News, slug=slug, is_published=True)
    return render(request, 'student/news/detail.html', {'article': article})
