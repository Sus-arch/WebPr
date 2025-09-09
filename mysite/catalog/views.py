from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Товар "{product.name}" успешно добавлен!')
            return redirect('catalog:product_detail', pk=product.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Товар "{product.name}" успешно обновлен!')
            return redirect('catalog:product_detail', pk=product.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form, 'product': product})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Товар "{product_name}" успешно удален!')
        return redirect('catalog:product_list')
    return render(request, 'catalog/product_confirm_delete.html', {'product': product})