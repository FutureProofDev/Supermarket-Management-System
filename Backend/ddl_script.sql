create database if not exists supermarket_db;
use supermarket_db;

create table supplier (
    supplier_id int auto_increment primary key,
    name varchar(100) not null,
    contact_phone varchar(20),
    email varchar(100) unique
);

create table category (
    category_id int auto_increment primary key,
    name varchar(50) not null unique
);

create table employee (
    employee_id int auto_increment primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    role varchar(50) not null,
    email varchar(100) unique
);

create table customer (
    customer_id int auto_increment primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    phone varchar(20) unique,
    email varchar(100) unique
);

create table discount (
    discount_id int auto_increment primary key,
    name varchar(100) not null,
    percent_off decimal(5,2) not null check (percent_off >= 0 and percent_off <= 100),
    start_date date not null,
    end_date date not null,
    check (end_date >= start_date)
);

create table product (
    product_id int auto_increment primary key,
    category_id int not null references category(category_id),
    supplier_id int not null references supplier(supplier_id),
    name varchar(100) not null,
    unit_price decimal(10,2) not null check (unit_price >= 0),
    barcode varchar(50) not null unique
);

create table purchase_order (
    po_id int auto_increment primary key,
    supplier_id int not null references supplier(supplier_id),
    order_date datetime not null default current_timestamp,
    status varchar(30) not null default 'Pending'
);

create table purchase_order_item (
    po_item_id int auto_increment primary key,
    po_id int not null references purchase_order(po_id),
    product_id int not null references product(product_id),
    quantity int not null check (quantity > 0),
    unit_cost decimal(10,2) not null check (unit_cost >= 0)
);

create table inventory (
    inventory_id int auto_increment primary key,
    product_id int not null unique references product(product_id),
    quantity_on_hand int not null default 0 check (quantity_on_hand >= 0),
    reorder_level int not null default 10 check (reorder_level >= 0)
);

create table sale (
    sale_id int auto_increment primary key,
    employee_id int not null references employee(employee_id),
    customer_id int references customer(customer_id),
    sale_date datetime not null default current_timestamp,
    total_amount decimal(10,2) not null default 0.00 check (total_amount >= 0)
);

create table sale_item (
    sale_item_id int auto_increment primary key,
    sale_id int not null references sale(sale_id),
    product_id int not null references product(product_id),
    discount_id int references discount(discount_id),
    quantity int not null check (quantity > 0),
    line_total decimal(10,2) not null check (line_total >= 0)
);

create table loyalty_card (
    card_id int auto_increment primary key,
    customer_id int not null unique references customer(customer_id),
    points_balance int not null default 0 check (points_balance >= 0),
    issued_date date not null default (current_date)
);


--  indexes for faster lookup
create index idx_product_name on product(name);
create index idx_customer_phone on customer(phone);
create index idx_sale_date on sale(sale_date);
create index idx_po_date on purchase_order(order_date);