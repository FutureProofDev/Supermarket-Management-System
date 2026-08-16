use supermarket_backup_db;

--  Suppliers 
insert into supplier (name, contact_phone, email) values
('Unilever Ghana PLC', '0302223401', 'orders@unileverghana.com'),
('Nestlé Ghana Limited', '0302500700', 'sales@gh.nestle.com'),
('FanMilk Ghana Limited', '0302224511', 'distributors@fanmilk-gh.com'),
('Kasapreko Company Limited', '0302810450', 'info@kasapreko.com'),
('GBfoods Ghana', '0302813930', 'ghana.sales@gbfoods.com'),
('Promasidor Ghana Limited', '0302810800', 'orders@promasidor.com.gh'),
('Blow Chem Industries (Bel Aqua)', '0302812345', 'sales@blowchem.com'),
('Accra Brewery Limited', '0302688081', 'info@abl.com.gh'),
('Guinness Ghana Breweries PLC', '0302810999', 'orders@guinnessghana.com'),
('Cocoa Processing Company Ltd', '0303212101', 'sales@golden-tree.com');

-- Categories
insert into category (name) values
('Dairy & Beverages'),
('Snacks & Confectionery'),
('Groceries & Staples'),
('Personal Care & Hygiene'),
('Household & Cleaning'),
('Alcoholic Beverages');

-- Employees
insert into employee (first_name, last_name, role, email) values
('Kwesi', 'Mensah', 'Store Manager', 'kwesi.mensah@supermarket.gh'),
('Ama', 'Osei', 'Head Cashier', 'ama.osei@supermarket.gh'),
('Yaw', 'Addo', 'Cashier', 'yaw.addo@supermarket.gh'),
('Efia', 'Appiah', 'Inventory Officer', 'efia.appiah@supermarket.gh'),
('Kwame', 'Boateng', 'Cashier', 'kwame.boateng@supermarket.gh');

-- Discounts
insert into discount (name, percent_off, start_date, end_date) values
('Easter Promo', 10.00, '2026-04-01', '2026-04-20'),
('Homowo Special', 15.00, '2026-08-01', '2026-08-31'),
('Farmers Day Discount', 5.00, '2026-12-01', '2026-12-10');

--  Customers 
insert into customer (first_name, last_name, phone, email) values
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
('Bernice', 'Opoku', '0244333340', 'bernice.opoku@gmail.com');

-- Products 
insert into product (category_id, supplier_id, name, unit_price, barcode) values
(1, 2, 'Ideal Milk 160g Tin', 8.50, 'GH0001001'),
(1, 2, 'Milo 400g Tin', 38.00, 'GH0001002'),
(1, 3, 'FanYogo Strawberry 145ml', 4.00, 'GH0001003'),
(1, 3, 'FanChoco 145ml', 4.00, 'GH0001004'),
(3, 5, 'Gino Tomato Paste 70g Sachet', 3.50, 'GH0001005'),
(3, 1, 'Frytol Vegetable Oil 1L', 45.00, 'GH0001006'),
(3, 5, 'Indomie Onion Chicken 70g', 3.00, 'GH0001007'),
(6, 8, 'Club Premium Lager 625ml', 14.00, 'GH0001008'),
(6, 8, 'Eagle Extra Stout 500ml', 12.00, 'GH0001009'),
(6, 4, 'Alomo Bitters 750ml', 35.00, 'GH0001010'),
(2, 10, 'Golden Tree Kingsbite Chocolate 50g', 12.00, 'GH0001011'),
(1, 2, 'Nescafé 3-in-1 Classic Sachet', 2.50, 'GH0001012'),
(1, 6, 'Cowbell Milk Powder 400g Sachet', 28.00, 'GH0001013'),
(1, 6, 'YumVita Infant Cereal 250g', 22.00, 'GH0001014'),
(1, 7, 'Bel-Aqua Mineral Water 1.5L', 5.00, 'GH0001015'),
(1, 7, 'Awake Purified Water 500ml', 2.50, 'GH0001016'),
(3, 1, 'Geisha Mackerel Tomato Sauce 425g', 24.00, 'GH0001017'),
(3, 1, 'Royco Beef Seasoning Cubes (50 Pack)', 18.00, 'GH0001018'),
(3, 5, 'Joff Rice Fragrant Rice 5kg', 110.00, 'GH0001019'),
(3, 1, 'Key Soap 800g Bar', 22.00, 'GH0001020'),
(4, 1, 'Geisha Aloe Vera Soap 150g', 8.00, 'GH0001021'),
(4, 1, 'Pepsodent Cavity Fighter 175g', 16.00, 'GH0001022'),
(5, 1, 'Omo Multi-Active Washing Powder 500g', 18.00, 'GH0001023'),
(5, 1, 'Sunlight Dishwashing Liquid 750ml', 25.00, 'GH0001024'),
(1, 9, 'Malta Guinness 330ml Can', 9.00, 'GH0001025'),
(1, 9, 'Alvaro Pear Drink 330ml Bottle', 8.50, 'GH0001026'),
(1, 7, 'Bel-Cola 500ml', 4.50, 'GH0001027'),
(1, 7, 'Squeeze Orange Juice 1L', 18.00, 'GH0001028'),
(1, 8, 'Beta Malt 330ml Pet Bottle', 8.00, 'GH0001029'),
(2, 6, 'Miksi Chocolate Powder 30g Sachet', 2.00, 'GH0001030'),
(2, 10, 'Golden Tree Akuafo Bar 50g', 12.00, 'GH0001031'),
(2, 3, 'FanIce Vanilla 145ml', 5.00, 'GH0001032'),
(1, 7, 'Bel-Chill Mango Juice 330ml', 4.00, 'GH0001033'),
(2, 6, 'Loya Milk Powder 30g Sachet', 2.20, 'GH0001034'),
(1, 2, 'Cerelac Wheat 400g Tin', 42.00, 'GH0001035'),
(1, 7, 'Rush Energy Drink 500ml', 6.00, 'GH0001036'),
(1, 7, 'Storm Energy Drink 500ml', 6.00, 'GH0001037'),
(3, 5, 'Poma Tomato Paste 400g Tin', 14.00, 'GH0001038'),
(6, 4, 'Kasapreko Carnival Strawberry 750ml', 40.00, 'GH0001039'),
(6, 9, 'Guinness Foreign Extra Stout 330ml', 13.00, 'GH0001040');

-- Inventory 
insert into inventory (product_id, quantity_on_hand, reorder_level) values
(1, 150, 30), (2, 80, 20), (3, 200, 50), (4, 180, 50), (5, 300, 60),
(6, 60, 15), (7, 500, 100), (8, 120, 30), (9, 90, 20), (10, 45, 10),
(11, 75, 15), (12, 400, 80), (13, 90, 20), (14, 50, 10), (15, 250, 40),
(16, 300, 50), (17, 110, 25), (18, 70, 15), (19, 40, 10), (20, 100, 20),
(21, 130, 25), (22, 95, 20), (23, 85, 20), (24, 60, 15), (25, 220, 40),
(26, 140, 30), (27, 180, 35), (28, 55, 10), (29, 130, 25), (30, 350, 70),
(31, 80, 15), (32, 160, 40), (33, 190, 40), (34, 310, 60), (35, 45, 10),
(36, 210, 40), (37, 230, 40), (38, 90, 20), (39, 35, 10), (40, 160, 30);

-- Purchase Orders
insert into purchase_order (supplier_id, order_date, status) values
(1, '2026-07-10 09:30:00', 'Received'),
(2, '2026-07-15 11:15:00', 'Received'),
(3, '2026-07-20 14:00:00', 'Received'),
(7, '2026-08-01 10:00:00', 'Pending');

-- Purchase Order Items
insert into purchase_order_item (po_id, product_id, quantity, unit_cost) values
(1, 6, 100, 38.00),
(1, 20, 150, 18.00),
(2, 1, 200, 6.80),
(2, 2, 100, 31.00),
(3, 3, 300, 3.10),
(4, 15, 500, 3.80);

-- Sales Transactions
insert into sale (employee_id, customer_id, sale_date, total_amount) values
(2, 1, '2026-08-02 10:15:00', 82.50),
(3, 2, '2026-08-03 12:30:00', 155.00),
(2, 5, '2026-08-04 14:10:00', 45.00),
(5, 12, '2026-08-05 16:45:00', 210.00),
(3, null, '2026-08-06 09:20:00', 36.00);

-- Sale Items
insert into sale_item (sale_id, product_id, discount_id, quantity, line_total) values
(1, 1, null, 2, 17.00),
(1, 2, null, 1, 38.00),
(1, 21, null, 1, 8.00),
(1, 22, null, 1, 16.00),
(2, 6, null, 1, 45.00),
(2, 19, 2, 1, 93.50),
(2, 5, null, 2, 7.00),
(3, 8, null, 2, 28.00),
(3, 25, null, 1, 9.00),
(3, 4, null, 2, 8.00),
(4, 10, null, 2, 70.00),
(4, 39, null, 1, 40.00),
(4, 40, null, 10, 130.00),
(5, 36, null, 6, 36.00);

-- Loyalty Cards 
insert into loyalty_card (customer_id, points_balance, issued_date) values
(1, 82, '2026-01-15'),
(2, 155, '2026-02-01'),
(5, 45, '2026-03-10'),
(12, 210, '2026-05-20'),
(13, 120, '2026-06-11');