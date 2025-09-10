from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
import datetime


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Аккаунт {username} успешно создан!', extra_tags='registration_success')
            return redirect('homepage:home')
        else:
            pass
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def cookie_demo(request):
    # Чтение куки
    visit_count = int(request.COOKIES.get('visit_count', 0))
    last_visit = request.COOKIES.get('last_visit', 'Никогда')

    # Увеличение счетчика посещений
    visit_count += 1

    # Установка текущего времени как времени последнего посещения
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Создание ответа
    response = render(request, 'cookie_demo.html', {
        'visit_count': visit_count,
        'last_visit': last_visit,
        'current_time': now,
    })

    # Установка куки
    response.set_cookie('visit_count', visit_count, max_age=3600 * 24 * 30)  # 30 дней
    response.set_cookie('last_visit', now, max_age=3600 * 24 * 30)

    return response


def set_cookie(request):
    # Установка простой куки
    response = HttpResponse("Куки установлены!")
    response.set_cookie('test_cookie', 'test_value', max_age=3600)
    response.set_cookie('user_preference', 'dark_theme', max_age=3600 * 24 * 7)
    return response


def get_cookie(request):
    # Чтение куки
    test_value = request.COOKIES.get('test_cookie', 'не установлено')
    preference = request.COOKIES.get('user_preference', 'не установлено')

    return HttpResponse(f"test_cookie: {test_value}, user_preference: {preference}")


def delete_cookie(request):
    # Удаление куки
    response = HttpResponse("Куки удалены!")
    response.delete_cookie('test_cookie')
    response.delete_cookie('user_preference')
    return response

class CustomLogoutView(View):
    @method_decorator(csrf_protect)
    def get(self, request):
        return render(request, 'registration/logout_confirm.html')

    def post(self, request):
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.', extra_tags='logout')
        return redirect('homepage:home')