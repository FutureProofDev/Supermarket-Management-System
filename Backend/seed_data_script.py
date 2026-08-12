# store/migrations/0002_seed_initial_data.py

from django.db import migrations
from django.utils import timezone
from datetime import datetime, date, timedelta

def populate_seed_data(apps, schema_editor):
    # Retrieve historical model versions
    Supplier = apps.get_model('store', 'Supplier')
    Category = apps.get_model('store', 'Category')
    Employee = apps.get_model('store', 'Employee')
    Discount = apps.get_model('store', 'Discount')
    Customer = apps.get_model('store', 'Customer')
    Product = apps.get_model('store', 'Product')
    Inventory = apps.get_model('store', 'Inventory')
    PurchaseOrder = apps.get_model('store', 'PurchaseOrder')
    PurchaseOrderItem = apps.get_model('store', 'PurchaseOrderItem')
    Sale = apps.get_model('store', 'Sale')
    SaleItem = apps.get_model('store', 'SaleItem')
    LoyaltyCard = apps.get_model('store', 'LoyaltyCard')

    # ==================== 1. SUPPLIERS ====================
    suppliers_data = [
        ('Unilever Ghana PLC', '0302223401', 'orders@unileverghana.com'),
        ('Nestlé Ghana Limited', '0302500700', 'sales@gh.nestle.com'),
        ('FanMilk Ghana Limited', '0302224511', 'distributors@fanmilk-gh.com'),
        ('Kasapreko Company Limited', '0302810450', 'info@kasapreko.com'),
        ('GBfoods Ghana', '0302813930', 'ghana.sales@gbfoods.com'),
        ('Promasidor Ghana Limited', '0302810800', 'orders@promasidor.com.gh'),
        ('Blow Chem Industries (Bel Aqua)', '0302812345', 'sales@blowchem.com'),
        ('Accra Brewery Limited', '0302688081', 'info@abl.com.gh'),
        ('Guinness Ghana Breweries PLC', '0302810999', 'orders@guinnessghana.com'),
        ('Cocoa Processing Company Ltd', '0303212101', 'sales@golden-tree.com'),
    ]
    suppliers = Supplier.objects.bulk_create([
        Supplier(name=name, contact_phone=phone, email=email)
        for name, phone, email in suppliers_data
    ])

    # ==================== 2. CATEGORIES (Expanded with Descriptions) ====================
    categories_data = [
        ('Dairy & Beverages', 'Fresh and canned milk, cocoa drinks, fruit juices, mineral water, and soft drinks.'),
        ('Snacks & Confectionery', 'Local chocolates, biscuits, ice creams, pouch snacks, and sweet treats.'),
        ('Groceries & Staples', 'Rice, vegetable oils, tomato pastes, instant noodles, canned fish, and seasonings.'),
        ('Personal Care & Hygiene', 'Bathing soaps, toothpaste, skincare products, and personal hygiene items.'),
        ('Household & Cleaning', 'Laundry detergents, dishwashing liquids, bar soaps, and cleaning chemicals.'),
        ('Alcoholic Beverages', 'Premium lagers, stouts, herbal bitters, wines, and alcoholic spirit drinks.'),
    ]
    categories = Category.objects.bulk_create([
        Category(name=name, description=desc)
        for name, desc in categories_data
    ])

    # ==================== 3. EMPLOYEES ====================
    employees_data = [
        ('Kwesi', 'Mensah', 'Store Manager', 'kwesi.mensah@supermarket.gh', '0240000001'),
        ('Ama', 'Osei', 'Head Cashier', 'ama.osei@supermarket.gh', '0240000002'),
        ('Yaw', 'Addo', 'Cashier', 'yaw.addo@supermarket.gh', '0240000003'),
        ('Efia', 'Appiah', 'Inventory Officer', 'efia.appiah@supermarket.gh', '0240000004'),
        ('Kwame', 'Boateng', 'Cashier', 'kwame.boateng@supermarket.gh', '0240000005'),
    ]
    employees = Employee.objects.bulk_create([
        Employee(first_name=fn, last_name=ln, role=role, email=email, phone=phone)
        for fn, ln, role, email, phone in employees_data
    ])

    # ==================== 4. DISCOUNTS ====================
    discounts_data = [
        ('Easter Promo', 10.00, date(2026, 4, 1), date(2026, 4, 20)),
        ('Homowo Special', 15.00, date(2026, 8, 1), date(2026, 8, 31)),
        ('Farmers Day Discount', 5.00, date(2026, 12, 1), date(2026, 12, 10)),
    ]
    discounts = Discount.objects.bulk_create([
        Discount(name=name, percent_off=pct, start_date=sd, end_date=ed)
        for name, pct, sd, ed in discounts_data
    ])

    # ==================== 5. CUSTOMERS ====================
    customers_raw = [
        ('Kofi', 'Agyemang', '0244100001', 'kofi.agyemang@gmail.com'),
        ('Abena', 'Dankwa', '0208200002', 'abena.dankwa@yahoo.com'),
        ('Kwabena', 'Frimpong', '0553300003', 'k.frimpong@outlook.com'),
        ('Akosua', 'Kyei', '0245400004', 'akosua.kyei@gmail.com'),
        ('Kojo', 'Antwi', '0501500005', 'kojo.antwi@hotmail.com'),
        ('Yaa', 'Asantewaa', '0246600006', 'yaa.asantewaa@gmail.com'),
        ('Kwaku', 'Sarpong', '0277700007', 'kwaku.sarpong@yahoo.com'),
        ('Afia', 'Acheampong', '0208800008', 'afia.ach@gmail.com'),
        ('Mawuli', 'Dogbe', '0549900009', 'mawuli.dogbe@gmail.com'),
        ('Selorm', 'Gbeku', '0241010010', 'selorm.gbeku@yahoo.com'),
        ('Kekeli', 'Avoke', '0502120011', 'kekeli.avoke@gmail.com'),
        ('Esi', 'Quaye', '0273230012', 'esi.quaye@hotmail.com'),
        ('Nii', 'Armah', '0244340013', 'nii.armah@gmail.com'),
        ('Naa', 'Lartey', '0205450014', 'naa.lartey@yahoo.com'),
        ('Kpakpo', 'Allotey', '0556560015', 'kpakpo.allotey@gmail.com'),
        ('Fuseini', 'Iddrisu', '0247670016', 'fuseini.iddrisu@gmail.com'),
        ('Aisha', 'Mohammed', '0508780017', 'aisha.m@yahoo.com'),
        ('Ibrahim', 'Yakubu', '0279890018', 'ibrahim.yakubu@hotmail.com'),
        ('Aminu', 'Bawa', '0241001019', 'aminu.bawa@gmail.com'),
        ('Fatima', 'Alhassan', '0202112020', 'fatima.alhassan@yahoo.com'),
        ('Kobina', 'Eshun', '0553223021', 'kobina.eshun@gmail.com'),
        ('Araba', 'Forson', '0244334022', 'araba.forson@gmail.com'),
        ('Ekow', 'Baidoo', '0505445023', 'ekow.baidoo@hotmail.com'),
        ('Adwoa', 'Sackey', '0276556024', 'adwoa.sackey@yahoo.com'),
        ('Ato', 'Crentsil', '0247667025', 'ato.crentsil@gmail.com'),
        ('Mavis', 'Ofori', '0208778026', 'mavis.ofori@gmail.com'),
        ('Gideon', 'Amoah', '0559889027', 'gideon.amoah@yahoo.com'),
        ('Grace', 'Boadu', '0241000128', 'grace.boadu@gmail.com'),
        ('Emmanuel', 'Tetteh', '0502111229', 'emmanuel.tetteh@hotmail.com'),
        ('Priscilla', 'Owusu', '0273222330', 'priscilla.owusu@yahoo.com'),
        ('Samuel', 'Gyamfi', '0244333431', 'samuel.gyamfi@gmail.com'),
        ('Rita', 'Donkor', '0205444532', 'rita.donkor@gmail.com'),
        ('Daniel', 'Asare', '0556555633', 'daniel.asare@yahoo.com'),
        ('Patience', 'Agyei', '0247666734', 'patience.agyei@gmail.com'),
        ('Francis', 'Nartey', '0508777835', 'francis.nartey@hotmail.com'),
        ('Joyce', 'Darko', '0279888936', 'joyce.darko@yahoo.com'),
        ('Ebenezer', 'Annan', '0241000037', 'ebenezer.annan@gmail.com'),
        ('Mercy', 'Aidoo', '0202111138', 'mercy.aidoo@gmail.com'),
        ('Isaac', 'Kwarteng', '0553222239', 'isaac.kwarteng@yahoo.com'),
        ('Bernice', 'Opoku', '0244333340', 'bernice.opoku@gmail.com'),
    ]
    customers = Customer.objects.bulk_create([
        Customer(first_name=fn, last_name=ln, phone=ph, email=em)
        for fn, ln, ph, em in customers_raw
    ])

    # ==================== 6. PRODUCTS ====================
    # Set sample expiry dates on select perishables (near expiry vs long shelf life)
    today = date.today()
    products_raw = [
        (1, 2, 'Ideal Milk 160g Tin', 8.50, 'GH0001001', today + timedelta(days=20)), # Near expiry (<45 days)
        (1, 2, 'Milo 400g Tin', 38.00, 'GH0001002', today + timedelta(days=180)),
        (1, 3, 'FanYogo Strawberry 145ml', 4.00, 'GH0001003', today + timedelta(days=15)), # Near expiry
        (1, 3, 'FanChoco 145ml', 4.00, 'GH0001004', today + timedelta(days=25)), # Near expiry
        (3, 5, 'Gino Tomato Paste 70g Sachet', 3.50, 'GH0001005', None),
        (3, 1, 'Frytol Vegetable Oil 1L', 45.00, 'GH0001006', None),
        (3, 5, 'Indomie Onion Chicken 70g', 3.00, 'GH0001007', today + timedelta(days=90)),
        (6, 8, 'Club Premium Lager 625ml', 14.00, 'GH0001008', None),
        (6, 8, 'Eagle Extra Stout 500ml', 12.00, 'GH0001009', None),
        (6, 4, 'Alomo Bitters 750ml', 35.00, 'GH0001010', None),
        (2, 10, 'Golden Tree Kingsbite Chocolate 50g', 12.00, 'GH0001011', today + timedelta(days=30)), # Near expiry
        (1, 2, 'Nescafé 3-in-1 Classic Sachet', 2.50, 'GH0001012', None),
        (1, 6, 'Cowbell Milk Powder 400g Sachet', 28.00, 'GH0001013', None),
        (1, 6, 'YumVita Infant Cereal 250g', 22.00, 'GH0001014', today + timedelta(days=120)),
        (1, 7, 'Bel-Aqua Mineral Water 1.5L', 5.00, 'GH0001015', None),
        (1, 7, 'Awake Purified Water 500ml', 2.50, 'GH0001016', None),
        (3, 1, 'Geisha Mackerel Tomato Sauce 425g', 24.00, 'GH0001017', None),
        (3, 1, 'Royco Beef Seasoning Cubes (50 Pack)', 18.00, 'GH0001018', None),
        (3, 5, 'Joff Rice Fragrant Rice 5kg', 110.00, 'GH0001019', None),
        (3, 1, 'Key Soap 800g Bar', 22.00, 'GH0001020', None),
        (4, 1, 'Geisha Aloe Vera Soap 150g', 8.00, 'GH0001021', None),
        (4, 1, 'Pepsodent Cavity Fighter 175g', 16.00, 'GH0001022', None),
        (5, 1, 'Omo Multi-Active Washing Powder 500g', 18.00, 'GH0001023', None),
        (5, 1, 'Sunlight Dishwashing Liquid 750ml', 25.00, 'GH0001024', None),
        (1, 9, 'Malta Guinness 330ml Can', 9.00, 'GH0001025', None),
        (1, 9, 'Alvaro Pear Drink 330ml Bottle', 8.50, 'GH0001026', None),
        (1, 7, 'Bel-Cola 500ml', 4.50, 'GH0001027', None),
        (1, 7, 'Squeeze Orange Juice 1L', 18.00, 'GH0001028', today + timedelta(days=10)), # Near expiry
        (1, 8, 'Beta Malt 330ml Pet Bottle', 8.00, 'GH0001029', None),
        (2, 6, 'Miksi Chocolate Powder 30g Sachet', 2.00, 'GH0001030', None),
        (2, 10, 'Golden Tree Akuafo Bar 50g', 12.00, 'GH0001031', None),
        (2, 3, 'FanIce Vanilla 145ml', 5.00, 'GH0001032', today + timedelta(days=14)), # Near expiry
        (1, 7, 'Bel-Chill Mango Juice 330ml', 4.00, 'GH0001033', None),
        (2, 6, 'Loya Milk Powder 30g Sachet', 2.20, 'GH0001034', None),
        (1, 2, 'Cerelac Wheat 400g Tin', 42.00, 'GH0001035', None),
        (1, 7, 'Rush Energy Drink 500ml', 6.00, 'GH0001036', None),
        (1, 7, 'Storm Energy Drink 500ml', 6.00, 'GH0001037', None),
        (3, 5, 'Poma Tomato Paste 400g Tin', 14.00, 'GH0001038', None),
        (6, 4, 'Kasapreko Carnival Strawberry 750ml', 40.00, 'GH0001039', None),
        (6, 9, 'Guinness Foreign Extra Stout 330ml', 13.00, 'GH0001040', None),
    ]

    products = Product.objects.bulk_create([
        Product(
            category=categories[cat_idx - 1],
            supplier=suppliers[sup_idx - 1],
            name=name,
            unit_price=price,
            barcode=barcode,
            expiry_date=exp
        )
        for cat_idx, sup_idx, name, price, barcode, exp in products_raw
    ])

    # ==================== 7. INVENTORY ====================
    inventory_raw = [
        (150, 30), (80, 20), (200, 50), (180, 50), (300, 60),
        (60, 15), (500, 100), (120, 30), (90, 20), (45, 10),
        (75, 15), (400, 80), (90, 20), (50, 10), (250, 40),
        (300, 50), (110, 25), (70, 15), (40, 10), (100, 20),
        (130, 25), (95, 20), (85, 20), (60, 15), (220, 40),
        (140, 30), (180, 35), (55, 10), (130, 25), (350, 70),
        (80, 15), (160, 40), (190, 40), (310, 60), (45, 10),
        (210, 40), (230, 40), (90, 20), (35, 10), (160, 30)
    ]
    Inventory.objects.bulk_create([
        Inventory(product=products[idx], quantity_on_hand=qoh, reorder_level=rl)
        for idx, (qoh, rl) in enumerate(inventory_raw)
    ])

    # ==================== 8. PURCHASE ORDERS ====================
    po_raw = [
        (1, timezone.make_aware(datetime(2026, 7, 10, 9, 30)), 'Received'),
        (2, timezone.make_aware(datetime(2026, 7, 15, 11, 15)), 'Received'),
        (3, timezone.make_aware(datetime(2026, 7, 20, 14, 0)), 'Received'),
        (7, timezone.make_aware(datetime(2026, 8, 1, 10, 0)), 'Pending'),
    ]
    purchase_orders = PurchaseOrder.objects.bulk_create([
        PurchaseOrder(supplier=suppliers[sup_idx - 1], order_date=dt, status=st)
        for sup_idx, dt, st in po_raw
    ])

    # ==================== 9. PURCHASE ORDER ITEMS ====================
    po_items_raw = [
        (1, 6, 100, 38.00),
        (1, 20, 150, 18.00),
        (2, 1, 200, 6.80),
        (2, 2, 100, 31.00),
        (3, 3, 300, 3.10),
        (4, 15, 500, 3.80),
    ]
    PurchaseOrderItem.objects.bulk_create([
        PurchaseOrderItem(
            po=purchase_orders[po_idx - 1],
            product=products[prod_idx - 1],
            quantity=qty,
            unit_cost=cost
        )
        for po_idx, prod_idx, qty, cost in po_items_raw
    ])

    # ==================== 10. SALES ====================
    sales_raw = [
        (2, 1, timezone.make_aware(datetime(2026, 8, 2, 10, 15)), 82.50),
        (3, 2, timezone.make_aware(datetime(2026, 8, 3, 12, 30)), 155.00),
        (2, 5, timezone.make_aware(datetime(2026, 8, 4, 14, 10)), 45.00),
        (5, 12, timezone.make_aware(datetime(2026, 8, 5, 16, 45)), 210.00),
        (3, None, timezone.make_aware(datetime(2026, 8, 6, 9, 20)), 36.00),
    ]
    sales = Sale.objects.bulk_create([
        Sale(
            employee=employees[emp_idx - 1],
            customer=customers[cust_idx - 1] if cust_idx else None,
            sale_date=s_date,
            total_amount=total
        )
        for emp_idx, cust_idx, s_date, total in sales_raw
    ])

    # ==================== 11. SALE ITEMS ====================
    sale_items_raw = [
        (1, 1, None, 2, 17.00),
        (1, 2, None, 1, 38.00),
        (1, 21, None, 1, 8.00),
        (1, 22, None, 1, 16.00),
        (2, 6, None, 1, 45.00),
        (2, 19, 2, 1, 93.50),
        (2, 5, None, 2, 7.00),
        (3, 8, None, 2, 28.00),
        (3, 25, None, 1, 9.00),
        (3, 4, None, 2, 8.00),
        (4, 10, None, 2, 70.00),
        (4, 39, None, 1, 40.00),
        (4, 40, None, 10, 130.00),
        (5, 36, None, 6, 36.00),
    ]
    SaleItem.objects.bulk_create([
        SaleItem(
            sale=sales[sale_idx - 1],
            product=products[prod_idx - 1],
            discount=discounts[disc_idx - 1] if disc_idx else None,
            quantity=qty,
            line_total=ltotal
        )
        for sale_idx, prod_idx, disc_idx, qty, ltotal in sale_items_raw
    ])

    # ==================== 12. LOYALTY CARDS ====================
    loyalty_raw = [
        (1, 82, date(2026, 1, 15)),
        (2, 155, date(2026, 2, 1)),
        (5, 45, date(2026, 3, 10)),
        (12, 210, date(2026, 5, 20)),
        (13, 120, date(2026, 6, 11)),
    ]
    LoyaltyCard.objects.bulk_create([
        LoyaltyCard(
            customer=customers[cust_idx - 1],
            points_balance=pts,
            issued_date=idate
        )
        for cust_idx, pts, idate in loyalty_raw
    ])


def clear_seed_data(apps, schema_editor):
    """
    Reverse function allowing `python manage.py migrate store 0001` to wipe 
    the seed data without crashing foreign keys.
    """
    for model_name in [
        'LoyaltyCard', 'SaleItem', 'Sale', 'PurchaseOrderItem', 
        'PurchaseOrder', 'Inventory', 'Product', 'Customer', 
        'Discount', 'Employee', 'Category', 'Supplier'
    ]:
        model = apps.get_model('store', model_name)
        model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_seed_data, reverse_code=clear_seed_data),
    ]