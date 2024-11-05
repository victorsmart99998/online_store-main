# Online Store

This is a multi-vendor Ecommerce platform for seamless buying and selling

## Want to use this project?

1. Fork/Clone


## Table of Contents 
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Run the application](#run-the-application)
- [Run the tests](#run-the-tests)
- [Add data to the application](#add-data-to-the-application)
- [Copyright and License](#copyright-and-license)


### Prerequisites

Install the following prerequisites:

1. [Python 3.11.7](https://www.python.org/downloads/)
<br> This project uses **Django v4.2.13**. For Django to work, you must install a correct version of Python on your machine. More information [here](https://django.readthedocs.io/en/stable/faq/install.html).
2. [PostgreSQL](psycopg2-binary==2.9.9 arleady in the requirement.txt)
3. [Visual Studio Code](https://code.visualstudio.com/download) 
<br> you can use any code editor


### Installation

#### 1. Create a virtual environment

From the **root** directory, run:

```bash
python -m venv env
```

#### 2. Activate the virtual environment

From the **root** directory, run:

On macOS:

```bash
source env/bin/activate
```

On Windows:

```bash
env\scripts\activate
```

#### 3. Install required dependencies

From the **root** directory, run:

```bash
pip install -r requirements.txt
```


#### 6. Run migrations

From the **root** directory, run:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

#### 7. Create an admin user to access the Django Admin interface

From the **root** directory, run:

```bash
python manage.py createsuperuser
```

When prompted, enter a username, email, and password.


### Run the application

From the **root** directory, run:

```bash
python manage.py runserver
```


### Run the tests

From the **root** directory, run:

```bash
python manage.py test --pattern="tests.py"

```


### View the application

Go to http://127.0.0.1:8000/ to view the application.

### Add data to the application

Add data through Django Admin.

Go to http://127.0.0.1:8000/admin to access the Django Admin interface and sign in using the admin credentials.


### Copyright and License

Copyright © 2024 Ebufy. Code released under the MIT license.
