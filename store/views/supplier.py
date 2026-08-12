from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError

from ..models import Supplier
from ..forms import SupplierForm


def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')
    return render(request, 'store/supplier/supplier_list.html', {'suppliers': suppliers})


def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, 'store/supplier/supplier_detail.html', {'supplier': supplier})


def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier "{supplier.name}" created.')
            return redirect('supplier_detail', pk=supplier.pk)
    else:
        form = SupplierForm()
    return render(request, 'store/supplier/supplier_form.html', {'form': form, 'title': 'Add Supplier'})


def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, f'Supplier "{supplier.name}" updated.')
            return redirect('supplier_detail', pk=supplier.pk)
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'store/supplier/supplier_form.html', {'form': form, 'title': 'Edit Supplier'})


def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        try:
            supplier.delete()
        except ProtectedError:
            messages.error(
                request,
                f'Can\'t delete "{supplier.name}" — products or purchase orders are still linked to this supplier.'
            )
            return redirect('supplier_detail', pk=supplier.pk)
        messages.success(request, f'Supplier "{supplier.name}" deleted.')
        return redirect('supplier_list')
    return render(request, 'store/supplier/supplier_confirm_delete.html', {'supplier': supplier})