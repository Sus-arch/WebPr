from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
import datetime
import json
from django.http import JsonResponse


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
    visit_count = int(request.COOKIES.get('visit_count', 0))
    last_visit = request.COOKIES.get('last_visit', 'Никогда')

    visit_count += 1

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    response = render(request, 'cookie_demo.html', {
        'visit_count': visit_count,
        'last_visit': last_visit,
        'current_time': now,
    })

    response.set_cookie('visit_count', visit_count, max_age=3600 * 24 * 30)  # 30 дней
    response.set_cookie('last_visit', now, max_age=3600 * 24 * 30)

    return response


def set_cookie(request):
    response = HttpResponse("Куки установлены!")
    response.set_cookie('test_cookie', 'test_value', max_age=3600)
    response.set_cookie('user_preference', 'dark_theme', max_age=3600 * 24 * 7)
    return response


def get_cookie(request):
    test_value = request.COOKIES.get('test_cookie', 'не установлено')
    preference = request.COOKIES.get('user_preference', 'не установлено')

    return HttpResponse(f"test_cookie: {test_value}, user_preference: {preference}")


def delete_cookie(request):
    response = HttpResponse("Куки удалены!")
    response.delete_cookie('test_cookie')
    response.delete_cookie('user_preference')
    return response


def cart_view(request):
    cart_json = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart_json)

    return render(request, 'cart.html', {'cart': cart})


def add_to_cart(request, product_id):
    cart_json = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart_json)

    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1

    response = JsonResponse({'status': 'success', 'cart': cart})

    response.set_cookie('cart', json.dumps(cart), max_age=3600 * 24 * 7)

    return response


def remove_from_cart(request, product_id):
    cart_json = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart_json)

    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]

    response = JsonResponse({'status': 'success', 'cart': cart})

    response.set_cookie('cart', json.dumps(cart), max_age=3600 * 24 * 7)

    return response


class CustomLogoutView(View):
    @method_decorator(csrf_protect)
    def get(self, request):
        return render(request, 'registration/logout_confirm.html')

    def post(self, request):
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.', extra_tags='logout')
        return redirect('homepage:home')