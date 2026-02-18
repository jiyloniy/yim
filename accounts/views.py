from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from student.forms import StudentLoginForm, StudentRegisterForm


def unified_login(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    form = StudentLoginForm()
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                messages.success(
                    request,
                    f"Xush kelibsiz, {user.get_full_name() or user.username}!",
                )
                # next parametri bo'lsa shu yerga redirect
                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return _redirect_by_role(user)
            else:
                messages.error(request, "Login yoki parol xato!")
    return render(request, 'student/login.html', {'form': form})


def unified_logout(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect('login')


def unified_register(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    form = StudentRegisterForm()
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            return _redirect_by_role(user)
    return render(request, 'student/register.html', {'form': form})


def _redirect_by_role(user):
    """Foydalanuvchi roliga qarab yo'naltirish."""
    if user.is_admin_user:
        return redirect('dashboard:home')
    return redirect('student:home')
