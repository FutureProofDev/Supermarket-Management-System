from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from ..models import Inventory
from ..forms import InventoryForm
from django.contrib.auth.decorators import permission_required


@permission_required('store.view_inventory', raise_exception=True)
def inventory_list(request):
    inventory = Inventory.objects.select_related('product').order_by('product__name')
    return render(request, 'store/inventory/inventory_list.html', {'inventory': inventory})


@permission_required('store.view_inventory', raise_exception=True)
def inventory_detail(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    return render(request, 'store/inventory/inventory_detail.html', {'item': item})


@permission_required('store.add_inventory', raise_exception=True)
def inventory_create(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f'Inventory record for "{item.product.name}" created.')
            return redirect('inventory_detail', pk=item.pk)
    else:
        form = InventoryForm()
    return render(request, 'store/inventory/inventory_form.html', {'form': form, 'title': 'Add Inventory Record'})


@permission_required('store.change_inventory', raise_exception=True)
def inventory_update(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Inventory record for "{item.product.name}" updated.')
            return redirect('inventory_detail', pk=item.pk)
    else:
        form = InventoryForm(instance=item)
    return render(request, 'store/inventory/inventory_form.html', {'form': form, 'title': 'Edit Inventory Record'})


@permission_required('store.delete_inventory', raise_exception=True)
def inventory_delete(request, pk):
    # Inventory has no incoming FKs from anything else. Nothing points to an Inventory row, so ProtectedError can't happen here.
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        product_name = item.product.name
        item.delete()
        messages.success(request, f'Inventory record for "{product_name}" deleted.')
        return redirect('inventory_list')
    return render(request, 'store/inventory/inventory_confirm_delete.html', {'item': item})