from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    template_name = 'homepage/index.html'

    return render(request, template_name)

def user(request):
    age = request.GET.get("age")
    name = request.GET.get("name")
    return HttpResponse(f"<h2>Имя: {name}  Возраст: {age}</h2>")
