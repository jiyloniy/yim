from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from functools import wraps

from accounts.models import User
from .models import (
    Laboratory, Program, Event, Project,
    Partner, Application, Certificate, News, SiteSetting
)
from .forms import (
    LoginForm, LaboratoryForm, ProgramForm, EventForm, ProjectForm,
    PartnerForm, CertificateForm, NewsForm, UserForm, UserCreateForm,
    SiteSettingForm
)


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin_user:
            messages.error(request, "Sizda ruxsat yo'q!")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# ==================== AUTH ====================

def admin_login(request):
    if request.user.is_authenticated and request.user.is_admin_user:
        return redirect('dashboard:home')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user and user.is_admin_user:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.get_full_name() or user.username}!")
                return redirect('dashboard:home')
            else:
                messages.error(request, "Login yoki parol xato, yoki sizda admin huquqi yo'q!")
    return render(request, 'dashboard/login.html', {'form': form})


def admin_logout(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect('login')


# ==================== DASHBOARD ====================

@admin_required
def dashboard_home(request):
    context = {
        'total_users': User.objects.count(),
        'total_students': User.objects.filter(role='student').count(),
        'total_labs': Laboratory.objects.filter(is_active=True).count(),
        'total_programs': Program.objects.filter(is_active=True).count(),
        'total_events': Event.objects.filter(is_active=True).count(),
        'total_projects': Project.objects.filter(is_active=True).count(),
        'total_partners': Partner.objects.filter(is_active=True).count(),
        'total_applications': Application.objects.count(),
        'pending_applications': Application.objects.filter(status='pending').count(),
        'total_news': News.objects.count(),
        'total_certificates': Certificate.objects.count(),
        'recent_applications': Application.objects.select_related('user', 'program')[:5],
        'recent_news': News.objects.all()[:5],
        'upcoming_events': Event.objects.filter(date__gte=timezone.now(), is_active=True)[:5],
    }
    return render(request, 'dashboard/home.html', context)


# ==================== GENERIC CRUD ====================

def generic_list(request, model, template, context_name, order_by='-created_at'):
    items = model.objects.all()
    search = request.GET.get('search', '')
    if search:
        if hasattr(model, 'name'):
            items = items.filter(name__icontains=search)
        elif hasattr(model, 'title'):
            items = items.filter(title__icontains=search)
    return render(request, template, {context_name: items, 'search': search})


def generic_create(request, form_class, template, redirect_url, success_msg):
    form = form_class()
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, success_msg)
            return redirect(redirect_url)
    return render(request, template, {'form': form})


def generic_edit(request, model, pk, form_class, template, redirect_url, success_msg):
    obj = get_object_or_404(model, pk=pk)
    form = form_class(instance=obj)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, success_msg)
            return redirect(redirect_url)
    return render(request, template, {'form': form, 'object': obj})


def generic_delete(request, model, pk, redirect_url, success_msg):
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, success_msg)
    return redirect(redirect_url)


# ==================== LABORATORIES ====================

@admin_required
def laboratory_list(request):
    return generic_list(request, Laboratory, 'dashboard/laboratories/list.html', 'laboratories', 'order')

@admin_required
def laboratory_create(request):
    return generic_create(request, LaboratoryForm, 'dashboard/laboratories/form.html', 'dashboard:laboratory_list', "Laboratoriya muvaffaqiyatli qo'shildi!")

@admin_required
def laboratory_edit(request, pk):
    return generic_edit(request, Laboratory, pk, LaboratoryForm, 'dashboard/laboratories/form.html', 'dashboard:laboratory_list', "Laboratoriya muvaffaqiyatli yangilandi!")

@admin_required
def laboratory_delete(request, pk):
    return generic_delete(request, Laboratory, pk, 'dashboard:laboratory_list', "Laboratoriya o'chirildi!")


# ==================== PROGRAMS ====================

@admin_required
def program_list(request):
    return generic_list(request, Program, 'dashboard/programs/list.html', 'programs')

@admin_required
def program_create(request):
    return generic_create(request, ProgramForm, 'dashboard/programs/form.html', 'dashboard:program_list', "Dastur muvaffaqiyatli qo'shildi!")

@admin_required
def program_edit(request, pk):
    return generic_edit(request, Program, pk, ProgramForm, 'dashboard/programs/form.html', 'dashboard:program_list', "Dastur muvaffaqiyatli yangilandi!")

@admin_required
def program_delete(request, pk):
    return generic_delete(request, Program, pk, 'dashboard:program_list', "Dastur o'chirildi!")


# ==================== EVENTS ====================

@admin_required
def event_list(request):
    return generic_list(request, Event, 'dashboard/events/list.html', 'events')

@admin_required
def event_create(request):
    return generic_create(request, EventForm, 'dashboard/events/form.html', 'dashboard:event_list', "Tadbir muvaffaqiyatli qo'shildi!")

@admin_required
def event_edit(request, pk):
    return generic_edit(request, Event, pk, EventForm, 'dashboard/events/form.html', 'dashboard:event_list', "Tadbir muvaffaqiyatli yangilandi!")

@admin_required
def event_delete(request, pk):
    return generic_delete(request, Event, pk, 'dashboard:event_list', "Tadbir o'chirildi!")


# ==================== PROJECTS ====================

@admin_required
def project_list(request):
    return generic_list(request, Project, 'dashboard/projects/list.html', 'projects')

@admin_required
def project_create(request):
    return generic_create(request, ProjectForm, 'dashboard/projects/form.html', 'dashboard:project_list', "Loyiha muvaffaqiyatli qo'shildi!")

@admin_required
def project_edit(request, pk):
    return generic_edit(request, Project, pk, ProjectForm, 'dashboard/projects/form.html', 'dashboard:project_list', "Loyiha muvaffaqiyatli yangilandi!")

@admin_required
def project_delete(request, pk):
    return generic_delete(request, Project, pk, 'dashboard:project_list', "Loyiha o'chirildi!")

@admin_required
def project_toggle_approve(request, pk):
    project = Project.objects.get(pk=pk)
    project.is_approved = not project.is_approved
    project.save()
    status = "tasdiqlandi" if project.is_approved else "tasdiq bekor qilindi"
    messages.success(request, f'"{project.title}" loyihasi {status}!')
    return redirect('dashboard:project_list')


# ==================== PARTNERS ====================

@admin_required
def partner_list(request):
    items = Partner.objects.all()
    search = request.GET.get('search', '')
    if search:
        items = items.filter(name__icontains=search)
    return render(request, 'dashboard/partners/list.html', {'partners': items, 'search': search})

@admin_required
def partner_create(request):
    return generic_create(request, PartnerForm, 'dashboard/partners/form.html', 'dashboard:partner_list', "Hamkor muvaffaqiyatli qo'shildi!")

@admin_required
def partner_edit(request, pk):
    return generic_edit(request, Partner, pk, PartnerForm, 'dashboard/partners/form.html', 'dashboard:partner_list', "Hamkor muvaffaqiyatli yangilandi!")

@admin_required
def partner_delete(request, pk):
    return generic_delete(request, Partner, pk, 'dashboard:partner_list', "Hamkor o'chirildi!")


# ==================== APPLICATIONS ====================

@admin_required
def application_list(request):
    items = Application.objects.select_related('user', 'program').all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        items = items.filter(status=status_filter)
    return render(request, 'dashboard/applications/list.html', {
        'applications': items,
        'status_filter': status_filter,
    })

@admin_required
def application_status(request, pk):
    app = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'approved', 'rejected']:
            app.status = new_status
            app.save()
            messages.success(request, "Ariza holati yangilandi!")
    return redirect('dashboard:application_list')

@admin_required
def application_delete(request, pk):
    return generic_delete(request, Application, pk, 'dashboard:application_list', "Ariza o'chirildi!")


# ==================== CERTIFICATES ====================

@admin_required
def certificate_list(request):
    items = Certificate.objects.select_related('user', 'program').all()
    return render(request, 'dashboard/certificates/list.html', {'certificates': items})

@admin_required
def certificate_create(request):
    return generic_create(request, CertificateForm, 'dashboard/certificates/form.html', 'dashboard:certificate_list', "Sertifikat muvaffaqiyatli qo'shildi!")

@admin_required
def certificate_edit(request, pk):
    return generic_edit(request, Certificate, pk, CertificateForm, 'dashboard/certificates/form.html', 'dashboard:certificate_list', "Sertifikat muvaffaqiyatli yangilandi!")

@admin_required
def certificate_delete(request, pk):
    return generic_delete(request, Certificate, pk, 'dashboard:certificate_list', "Sertifikat o'chirildi!")


# ==================== NEWS ====================

@admin_required
def news_list(request):
    return generic_list(request, News, 'dashboard/news/list.html', 'news_items')

@admin_required
def news_create(request):
    return generic_create(request, NewsForm, 'dashboard/news/form.html', 'dashboard:news_list', "Yangilik muvaffaqiyatli qo'shildi!")

@admin_required
def news_edit(request, pk):
    return generic_edit(request, News, pk, NewsForm, 'dashboard/news/form.html', 'dashboard:news_list', "Yangilik muvaffaqiyatli yangilandi!")

@admin_required
def news_delete(request, pk):
    return generic_delete(request, News, pk, 'dashboard:news_list', "Yangilik o'chirildi!")


# ==================== USERS ====================

@admin_required
def user_list(request):
    items = User.objects.all()
    search = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    if search:
        items = items.filter(username__icontains=search) | items.filter(first_name__icontains=search) | items.filter(last_name__icontains=search)
    if role_filter:
        items = items.filter(role=role_filter)
    return render(request, 'dashboard/users/list.html', {
        'users': items,
        'search': search,
        'role_filter': role_filter,
    })

@admin_required
def user_create(request):
    form = UserCreateForm()
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Foydalanuvchi muvaffaqiyatli qo'shildi!")
            return redirect('dashboard:user_list')
    return render(request, 'dashboard/users/form.html', {'form': form})

@admin_required
def user_edit(request, pk):
    return generic_edit(request, User, pk, UserForm, 'dashboard/users/form.html', 'dashboard:user_list', "Foydalanuvchi muvaffaqiyatli yangilandi!")

@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "O'zingizni o'chira olmaysiz!")
        return redirect('dashboard:user_list')
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Foydalanuvchi o'chirildi!")
    return redirect('dashboard:user_list')


# ==================== SETTINGS ====================

@admin_required
def site_settings(request):
    settings_obj = SiteSetting.get_settings()
    form = SiteSettingForm(instance=settings_obj)
    if request.method == 'POST':
        form = SiteSettingForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Sozlamalar muvaffaqiyatli saqlandi!")
            return redirect('dashboard:site_settings')
    return render(request, 'dashboard/settings.html', {'form': form})
