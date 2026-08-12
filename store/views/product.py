from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from ..models import Product
from ..forms import ProductForm


def product_list(request):
    products = Product.objects.select_related('category', 'supplier').order_by('name')
    return render(request, 'store/product/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product/product_detail.html', {'product': product})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'store/product/product_form.html', {'form': form, 'title': 'Add Product'})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product/product_form.html', {'form': form, 'title': 'Edit Product'})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            product.delete()
        except ProtectedError:
            # Inventory.product, PurchaseOrderItem.product, SaleItem.product
            # are all PROTECT -- a product with stock/order/sale history
            # can't be silently deleted.
            messages.error(
                request,
                f'Can\'t delete "{product.name}" — it still has inventory, purchase, or sale records linked to it.'
            )
            return redirect('product_detail', pk=product.pk)
        messages.success(request, f'Product "{product.name}" deleted.')
        return redirect('product_list')
    return render(request, 'store/product/product_confirm_delete.html', {'product': product})