from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from ..models import Category
from ..forms import CategoryForm


@permission_required('store.view_category', raise_exception=True)
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'store/category/category_list.html', {'categories': categories})


@permission_required('store.view_category', raise_exception=True)
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'store/category/category_detail.html', {'category': category})


@permission_required('store.add_category', raise_exception=True)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'"{category.name}" created.')
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm()
    return render(request, 'store/category/category_form.html', {'form': form, 'title': 'Add Category'})


@permission_required('store.change_category', raise_exception=True)
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{category.name}" updated.')
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'store/category/category_form.html', {'form': form, 'title': 'Edit Category'})


@permission_required('store.delete_category', raise_exception=True)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        try:
            category.delete()
        except ProtectedError:
            messages.error(
                request,
                f'Can\'t delete "{category.name}" — one or more products still belong to it.'
            )
            return redirect('category_detail', pk=category.pk)
        messages.success(request, f'"{category.name}" deleted.')
        return redirect('category_list')
    return render(request, 'store/category/category_confirm_delete.html', {'category': category})