create database if not exists supermarket_db;
use supermarket_db;

create table supplier (
    supplier_id int auto_increment primary key,
    name varchar(100) not null,
    contact_phone varchar(20),
    email varchar(100)
);

create table category (
    category_id int auto_increment primary key,
    name varchar(50) not null
);

create table employee (
    employee_id int auto_increment primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    role varchar(50) not null,
    email varchar(100)
);

create table customer (
    customer_id int auto_increment primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    phone varchar(20),
    email varchar(100)
);

create table discount (
    discount_id int auto_increment primary key,
    name varchar(100) not null,
    percent_off decimal(5,2) not null,
    start_date date not null,
    end_date date not null
);

create table product (
    product_id int auto_increment primary key,
    category_id int not null references category(category_id),
    supplier_id int not null references supplier(supplier_id),
    name varchar(100) not null,
    unit_price decimal(10,2) not null,
    barcode varchar(50) not null unique
);

create table purchase_order (
    po_id int auto_increment primary key,
    supplier_id int not null references supplier(supplier_id),
    order_date datetime not null,
    status varchar(30) not null
);

create table purchase_order_item (
    po_item_id int auto_increment primary key,
    po_id int not null references purchase_order(po_id),
    product_id int not null references product(product_id),
    quantity int not null,
    unit_cost decimal(10,2) not null
);

create table inventory (
    inventory_id int auto_increment primary key,
    product_id int not null unique references product(product_id),
    quantity_on_hand int not null,
    reorder_level int not null
);

create table sale (
    sale_id int auto_increment primary key,
    employee_id int not null references employee(employee_id),
    customer_id int references customer(customer_id),
    sale_date datetime not null,
    total_amount decimal(10,2) not null
);

create table sale_item (
    sale_item_id int auto_increment primary key,
    sale_id int not null references sale(sale_id),
    product_id int not null references product(product_id),
    discount_id int references discount(discount_id),
    quantity int not null,
    line_total decimal(10,2) not null
);

create table loyalty_card (
    card_id int auto_increment primary key,
    customer_id int not null unique references customer(customer_id),
    points_balance int not null,
    issued_date date not null
);