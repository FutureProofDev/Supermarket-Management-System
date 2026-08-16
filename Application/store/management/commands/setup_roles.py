from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

# Store Manager isn't listed here — that role is granted by making the
# Django User a superuser (is_superuser=True), which bypasses permission
# checks entirely. These three groups cover the differentiated,
# restricted access levels.
ROLE_PERMISSIONS = {
    'Inventory Officer': {
        'product': ['add', 'change', 'delete', 'view'],
        'supplier': ['add', 'change', 'delete', 'view'],
        'category': ['add', 'change', 'delete', 'view'],
        'inventory': ['add', 'change', 'delete', 'view'],
        'purchaseorder': ['add', 'change', 'delete', 'view'],
        'purchaseorderitem': ['add', 'change', 'delete', 'view'],
        'sale': ['view'],
        'saleitem': ['view'],
        'customer': ['view'],
        'loyaltycard': ['view'],
        'discount': ['view'],
        'employee': ['view'],
    },
    'Head Cashier': {
        'sale': ['view', 'add'],
        'saleitem': ['add', 'view'],
        'customer': ['add', 'change', 'delete', 'view'],
        'loyaltycard': ['add', 'change', 'delete', 'view'],
        'discount': ['view'],
        'product': ['view'],
        'inventory': ['view'],
        'category': ['view'],
        'supplier': ['view'],
    },
    'Cashier': {
        'sale': ['view', 'add'],
        'saleitem': ['add', 'view'],
        'customer': ['add', 'view'],
        'loyaltycard': ['view'],
        'product': ['view'],
        'inventory': ['view'],
        'discount': ['view'],
    },
}


class Command(BaseCommand):
    help = 'Creates the Head Cashier, Cashier, and Inventory Officer groups with their model permissions.'

    def handle(self, *args, **options):
        for role_name, model_perms in ROLE_PERMISSIONS.items():
            group, _ = Group.objects.get_or_create(name=role_name)
            group.permissions.clear()

            for model_name, actions in model_perms.items():
                for action in actions:
                    codename = f'{action}_{model_name}'
                    try:
                        permission = Permission.objects.get(
                            codename=codename, content_type__app_label='store'
                        )
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f'Permission "{codename}" not found — skipping.'
                        ))

            self.stdout.write(self.style.SUCCESS(
                f'{role_name}: {group.permissions.count()} permissions set.'
            ))

        self.stdout.write(self.style.SUCCESS(
            'Role setup complete. Store Manager = Django superuser.'
        ))