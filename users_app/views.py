# users_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import (
    RegistrationForm,
    CustomAuthenticationForm,
    ProfileUpdateForm,
    PasswordChangeCustomForm
)
from .models import CustomUser


def register(request):
    if request.user.is_authenticated:
        return redirect('sport_app:sport_list')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
            return redirect('sport_app:sport_list')
    else:
        form = RegistrationForm()

    return render(request, 'users_app/register.html', {
        'form': form,
        'title': 'Регистрация'
    })


def user_login(request):
    if request.user.is_authenticated:
        return redirect('sport_app:sport_list')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.email}!')
                next_url = request.GET.get('next', 'sport_app:sport_list')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверный email или пароль')
        else:
            messages.error(request, 'Ошибка входа. Проверьте введенные данные.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users_app/login.html', {
        'form': form,
        'title': 'Вход в систему'
    })


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('users_app:login')


class ProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'users_app/profile_edit.html'
    success_url = reverse_lazy('users_app:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)


@login_required
def profile(request):
    return render(request, 'users_app/profile.html', {
        'user': request.user
    })


def update_session_auth_hash(request, user):
    pass


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('users_app:profile')
    else:
        form = PasswordChangeCustomForm(request.user)

    return render(request, 'users_app/change_password.html', {
        'form': form,
        'title': 'Смена пароля'
    })