from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import PurchaseOrder
from ..forms import PurchaseOrderForm


def purchaseorder_list(request):
    orders = PurchaseOrder.objects.select_related('supplier').order_by('-order_date')
    return render(request, 'store/purchase_order/purchaseorder_list.html', {'orders': orders})


def purchaseorder_detail(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    return render(request, 'store/purchase_order/purchaseorder_detail.html', {'order': order})


def purchaseorder_create(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, f'Purchase order #{order.po_id} created.')
            return redirect('purchaseorder_detail', pk=order.pk)
    else:
        form = PurchaseOrderForm()
    return render(request, 'store/purchase_order/purchaseorder_form.html', {'form': form, 'title': 'Add Purchase Order'})


def purchaseorder_update(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Purchase order #{order.po_id} updated.')
            return redirect('purchaseorder_detail', pk=order.pk)
    else:
        form = PurchaseOrderForm(instance=order)
    return render(request, 'store/purchase_order/purchaseorder_form.html', {'form': form, 'title': 'Edit Purchase Order'})


def purchaseorder_delete(request, pk):
    # PurchaseOrderItem.po is CASCADE -- deleting an order deletes its line
    # items too, so no ProtectedError is possible here. No try/except needed.
    order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        po_id = order.po_id
        order.delete()
        messages.success(request, f'Purchase order #{po_id} deleted.')
        return redirect('purchaseorder_list')
    return render(request, 'store/purchase_order/purchaseorder_confirm_delete.html', {'order': order})