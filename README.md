# Supermarket Management System

A Django + MySQL supermarket management system built for CS323 Database Systems. Supports role-based access control (Store Manager, Inventory Officer, Head Cashier, Cashier), full CRUD across all core entities, checkout/sales transactions, inventory tracking, and reporting.

## Group Members

- Nii Sowah Kwabla Sowah
- Natalie Rose Andzie-Mensah
- Yaa Waadu Asomaning
- Vladimir Noel Aduama

## Technologies Used

- **Backend:** Django (Python)
- **Database:** MySQL
- **Frontend:** Django Templates, HTML/CSS, JS

## Prerequisites

- Python 3.x and pip
- MySQL Server installed, with the `mysql` command-line client available (Workbench, MySQL CLI, or any client that lets you run `.sql` files works too)
- A virtual environment tool (`venv`)

## Setup Instructions
Run all commands below from an integrated terminal opened at the **project Application folder** (the same folder as `manage.py`).

If "mysql -u root -p" commands fail to run. Either add mysql to your system path or open a mysql client and ran the contents
of the .sql files directly in the terminal. 

### 1. Clone and set up the environment

```bash
git clone <repo-url>
cd supermarket_management_system
python -m venv .venv
```

Activate the virtual environment:
- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Generate a django secrete key with this command:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Create a `.env` file in the project root with your database credentials:

```
DB_NAME=supermarket_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
SECRET_KEY="your_django_secret_key"

```

### 3. Create the database schema

Open a MySQL client (command line or GUI) and run the following, in this exact order, against a fresh MySQL server:

```bash
mysql -u root -p < Database/create_database.sql
mysql -u root -p < Database/create_tables.sql
mysql -u root -p supermarket_db < Database/procedures.sql
mysql -u root -p supermarket_db < Database/queries.sql
mysql -u root -p supermarket_db < Database/triggers.sql
mysql -u root -p supermarket_db < Database/views.sql
```

This creates the `supermarket_db` database and all core application tables (`product`, `customer`, `employee`, `sale`, `inventory`, etc.), along with constraints and indexes.

### 4. Seed initial data

```bash
mysql -u root -p supermarket_db < Database/insert_data.sql
```

This populates suppliers, categories, employees, customers, products, inventory, purchase orders, sales, and loyalty cards with realistic sample data.

### 5. Let Django create its own internal tables

Django manages its own authentication and session tables (`auth_user`, `auth_group`, `django_session`, etc.), which the DDL script above does not create. Run:

```bash
python manage.py migrate auth
python manage.py migrate contenttypes
python manage.py migrate sessions
python manage.py migrate admin
```

### 6. Attach the Employee - User foreign key

The `employee.user_id` column links a staff record to a Django login account, but this foreign key can't be created until `auth_user` exists (step 5). Run the following against your database:

```bash
mysql -u root -p supermarket_db < Database/foreign_key.sql
```

### 7.  Django setup with existing tables

Since the schema was created manually via SQL rather than through `python manage.py migrate store`, tell Django to mark those migrations as already applied without re-running them:

```bash
python manage.py migrate store --fake
```

### 8. Set up roles and permissions

```bash
python manage.py setup_roles
```

This creates the **Inventory Officer**, **Head Cashier**, and **Cashier** groups with their correct model-level permissions. The **Store Manager** role is not a group. It's granted by making a Django user a superuser (superusers bypass all permission checks).

### 9. Create your Store Manager account

#### Django may prompt you in the terminal to fill out some information. Provide a username and password and leave the rest blank.

```bash
python manage.py createsuperuser
```

### 10. (Optional) Create additional test accounts per role

In `/admin/`, create additional `User` accounts, assign each to a Group (Inventory Officer / Head Cashier / Cashier), and link them to an `Employee` record via the employee's `User` dropdown — this is what allows that account to process sales under their name.

### 11. Run the server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and log in.



## Test Accounts

| Role | Username | Password | Notes |
|---|---|---|---|
| Store Manager | | | Superuser — full access |
| Head Cashier | | | Sales, customers, loyalty cards, daily report |
| Cashier | | | Sales, inventory (view), search |
| Inventory Officer | | | Products, suppliers, categories, inventory, purchase orders |

## Project Structure

```
Project/
├── database_backend/
│   ├── ddl_script.sql              
│   ├── ddl_script_generated.sql    
│   ├── dml_script.sql              
│   ├── foreign_key.sql             
│   ├── advanced_scripts.sql        
│   
├── store/
│   ├── migrations/
│   ├── management/commands/setup_roles.py
│   ├── models.py
│   ├── views/
│   ├── templates/
│   └── static/
├── supermarket_management_system/
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── README.md
```

