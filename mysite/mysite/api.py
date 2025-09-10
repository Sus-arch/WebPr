from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def api_products(request):
    from catalog.models import Product
    from django.core import serializers

    products = Product.objects.all()
    data = serializers.serialize('json', products)
    return JsonResponse({'products': data}, safe=False)


@require_http_methods(["GET"])
@login_required
def api_user_info(request):
    return JsonResponse({
        'username': request.user.username,
        'email': request.user.email,
        'is_authenticated': request.user.is_authenticated
    })