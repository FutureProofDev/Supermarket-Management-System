create database if not exists supermarket__db;
use supermarket__db;

-- drop existing tables in reverse dependency order
drop table if exists loyalty_card;
drop table if exists sale_item;
drop table if exists sale;
drop table if exists inventory;
drop table if exists purchase_order_item;
drop table if exists purchase_order;
drop table if exists product;
drop table if exists discount;
drop table if exists customer;
drop table if exists role_permission;
drop table if exists permission;
drop table if exists user_role;
drop table if exists role;
drop table if exists user;
drop table if exists employee;
drop table if exists category;
drop table if exists supplier;

-- Additional supermarket based  tables
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

-- Role based tables
create table employee (
    employee_id int auto_increment primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    email varchar(100) unique not null,
    phone varchar(20),
    hire_date date not null,
    shift varchar(30)
);

create table user (
    user_id int auto_increment primary key,
    employee_id int unique not null,
    username varchar(50) not null unique,
    password_hash varchar(255) not null,
    is_active boolean not null default true,
    constraint fk_user_employee foreign key (employee_id) references employee(employee_id) on delete cascade
);

create table role (
    role_id int auto_increment primary key,
    role_name varchar(50) not null unique,
    description varchar(255)
);

create table user_role (
    user_id int not null,
    role_id int not null,
    primary key (user_id, role_id),
    constraint fk_ur_user foreign key (user_id) references user(user_id) on delete cascade,
    constraint fk_ur_role foreign key (role_id) references role(role_id) on delete cascade
);

create table permission (
    permission_id int auto_increment primary key,
    permission_name varchar(100) not null unique,
    description varchar(255)
);

create table role_permission (
    role_id int not null,
    permission_id int not null,
    primary key (role_id, permission_id),
    constraint fk_rp_role foreign key (role_id) references role(role_id) on delete cascade,
    constraint fk_rp_permission foreign key (permission_id) references permission(permission_id) on delete cascade
);


--  Customer oriented tables
create table customer (
    customer_id int auto_increment primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    phone varchar(20) unique,
    email varchar(100) unique
);

create table loyalty_card (
    card_id int auto_increment primary key,
    customer_id int not null unique,
    points_balance int not null default 0 check (points_balance >= 0),
    issued_date date not null default (current_date),
    constraint fk_loyalty_customer foreign key (customer_id) references customer(customer_id) on delete cascade
);

create table discount (
    discount_id int auto_increment primary key,
    name varchar(100) not null,
    percent_off decimal(5,2) not null check (percent_off >= 0 and percent_off <= 100),
    start_date date not null,
    end_date date not null,
    constraint chk_discount_dates check (end_date >= start_date)
);


-- Record keeping tables
create table product (
    product_id int auto_increment primary key,
    category_id int not null,
    name varchar(100) not null,
    unit_price decimal(10,2) not null check (unit_price >= 0),
    barcode varchar(50) not null unique,
    constraint fk_product_category foreign key (category_id) references category(category_id)
);

create table inventory (
    inventory_id int auto_increment primary key,
    product_id int not null unique,
    quantity_on_hand int not null default 0 check (quantity_on_hand >= 0),
    reorder_level int not null default 10 check (reorder_level >= 0),
    constraint fk_inventory_product foreign key (product_id) references product(product_id) on delete cascade
);

-- Stock procurement tables
create table purchase_order (
    po_id int auto_increment primary key,
    supplier_id int not null,
    employee_id int not null,
    order_date datetime not null default current_timestamp,
    status varchar(30) not null default 'Pending',
    constraint fk_po_supplier foreign key (supplier_id) references supplier(supplier_id),
    constraint fk_po_employee foreign key (employee_id) references employee(employee_id)
);

create table purchase_order_item (
    po_item_id int auto_increment primary key,
    po_id int not null,
    product_id int not null,
    quantity int not null check (quantity > 0),
    unit_cost decimal(10,2) not null check (unit_cost >= 0),
    constraint fk_poi_po foreign key (po_id) references purchase_order(po_id) on delete cascade,
    constraint fk_poi_product foreign key (product_id) references product(product_id)
);

-- Sales & transactions
create table sale (
    sale_id int auto_increment primary key,
    employee_id int not null,
    customer_id int null,
    sale_date datetime not null default current_timestamp,
    total_amount decimal(10,2) not null default 0.00 check (total_amount >= 0),
    constraint fk_sale_employee foreign key (employee_id) references employee(employee_id),
    constraint fk_sale_customer foreign key (customer_id) references customer(customer_id) on delete set null
);

create table sale_item (
    sale_item_id int auto_increment primary key,
    sale_id int not null,
    product_id int not null,
    discount_id int null,
    quantity int not null check (quantity > 0),
    line_total decimal(10,2) not null check (line_total >= 0),
    constraint fk_si_sale foreign key (sale_id) references sale(sale_id) on delete cascade,
    constraint fk_si_product foreign key (product_id) references product(product_id),
    constraint fk_si_discount foreign key (discount_id) references discount(discount_id) on delete set null
);

-- Indexes for fast look up
create index idx_product_name on product(name);
create index idx_customer_phone on customer(phone);
create index idx_sale_date on sale(sale_date);
create index idx_po_date on purchase_order(order_date);
create index idx_user_username on user(username);