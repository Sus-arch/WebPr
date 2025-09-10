from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


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


class CustomLogoutView(View):
    @method_decorator(csrf_protect)
    def get(self, request):
        return render(request, 'registration/logout_confirm.html')

    def post(self, request):
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.', extra_tags='logout')
        return redirect('homepage:home')