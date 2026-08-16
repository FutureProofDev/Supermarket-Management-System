from django import forms
from .models import *
from django.forms import formset_factory 

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_phone', 'email']        


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'role', 'email']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email']


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['name', 'percent_off', 'start_date', 'end_date']       


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'supplier', 'name', 'unit_price', 'barcode', 'expiry_date']
        widgets = {'expiry_date': forms.DateInput(attrs={'type': 'date'})}


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'status']


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'quantity_on_hand', 'reorder_level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On create, only offer products that don't already have an
        # Inventory row (it's a OneToOne). On edit, keep the current
        # product selectable even though it "already has" this row.
        qs = Product.objects.filter(inventory__isnull=True)
        if self.instance.pk:
            qs = qs | Product.objects.filter(pk=self.instance.product_id)
        self.fields['product'].queryset = qs.order_by('name')


class LoyaltyCardForm(forms.ModelForm):
    class Meta:
        model = LoyaltyCard
        fields = ['customer', 'points_balance', 'issued_date']
        widgets = {'issued_date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Same OneToOne guard as Inventory, on Customer this time.
        qs = Customer.objects.filter(loyalty_card__isnull=True)
        if self.instance.pk:
            qs = qs | Customer.objects.filter(pk=self.instance.customer_id)
        self.fields['customer'].queryset = qs.order_by('last_name', 'first_name')         


class SaleHeaderForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False)


class SaleLineForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=False)
    quantity = forms.IntegerField(min_value=1, required=False)


SaleLineFormSet = formset_factory(SaleLineForm, extra=5)



from django import forms
from django.forms import formset_factory
from .models import Customer, Product


class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Displays name, unit price, and live quantity in the select dropdown
        qty = obj.inventory.quantity_on_hand if hasattr(obj, 'inventory') else 0
        return f"{obj.name} — GHS {obj.unit_price:.2f} ({qty} in stock)"


class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        qty = obj.inventory.quantity_on_hand if hasattr(obj, 'inventory') else 0
        expiry_badge = " [PROMO: 50% Near-Expiry]" if obj.is_near_expiry() else ""
        return f"{obj.name} — GHS {obj.unit_price:.2f} ({qty} in stock){expiry_badge}"


class SaleHeaderForm(forms.Form):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all().order_by('last_name', 'first_name'),
        required=False,
        empty_label="-- Walk-in Customer (No Loyalty Card) --",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'customer-select'})
    )
    discount = forms.ModelChoiceField(
        queryset=Discount.objects.none(),
        required=False,
        empty_label="-- No Promotional Discount --",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'discount-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.localdate()
        # Only show valid, currently active discounts
        self.fields['discount'].queryset = Discount.objects.filter(
            start_date__lte=today,
            end_date__gte=today
        ).order_by('-percent_off')


class SaleLineForm(forms.Form):
    product = ProductChoiceField(
        queryset=Product.objects.select_related('inventory').order_by('name'),
        required=False,
        empty_label="-- Select Product --",
        widget=forms.Select(attrs={'class': 'form-control product-select'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control qty-input', 'min': '1', 'placeholder': 'Qty'})
    )


SaleLineFormSet = formset_factory(SaleLineForm, extra=1)