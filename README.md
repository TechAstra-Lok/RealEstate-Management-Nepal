hamrogharjagga/                # Main project directory
│
├── home/                      # Home app directory
│   ├── __pycache__/           # Compiled Python files
│   ├── migrations/            # Database migrations
│   ├── templates/             # Template files
│   │   └── home/              # Template directory for home app
│   │       ├── base.html      # Base template file
│   │       ├── home.html      # Home page template
│   │       └── modals.html    # Modal template
│   ├── __init__.py            # Package initialization file
│   ├── admin.py               # Admin configurations
│   ├── apps.py                # App configuration
│   ├── forms.py               # Forms related to the app
│   ├── models.py              # Models for database
│   ├── tests.py               # Test cases (blank for now)
│   ├── urls.py                # URL routing for the app
│   └── views.py               # Views for handling requests
│
├── buyer/                     # Buyer app directory
│   ├── __pycache__/           # Compiled Python files
│   ├── migrations/            # Database migrations
│   ├── templates/             # Template files
│   │   └── home/              # Template directory for home app
│   │       ├── properties.html # Properties page template
│   │       └── wishlist.html  # Wishlist page template
│   ├── __init__.py            # Package initialization file
│   ├── admin.py               # Admin configurations
│   ├── apps.py                # App configuration
│   ├── models.py              # Models for database
│   ├── tests.py               # Test cases (blank for now)
│   ├── urls.py                # URL routing for the app
│   └── views.py               # Views for handling requests
│
├── seller/                    # Seller app directory
│   ├── __pycache__/           # Compiled Python files
│   ├── migrations/            # Database migrations
│   ├── templates/             # Template files
│   │   └── home/              # Template directory for home app
│   │       ├── sell_property.html # Property selling template
│   │       └── seller_dashboard.html # Seller dashboard template
│   ├── __init__.py            # Package initialization file
│   ├── admin.py               # Admin configurations
│   ├── apps.py                # App configuration
│   ├── models.py              # Models for database
│   ├── tests.py               # Test cases (blank for now)
│   ├── urls.py                # URL routing for the app
│   └── views.py               # Views for handling requests
│
├── hamrogharjagga/            # Project settings folder (internal folder)
│   ├── __init__.py            # Package initialization file
│   ├── settings.py            # Settings for the project (database, templates, static, etc.)
│   ├── urls.py                # URL routing for the main project
│   ├── asgi.py                # ASGI configuration for asynchronous support
│   └── wsgi.py                # WSGI configuration for deploying the project
│
├── venv/                      # Virtual environment directory
│
├── static/                    # Static files (CSS, JS, images)
├── db.sqlite3                 # SQLite database file
├── manage.py                  # Django management script
└── README.md                  # Project documentation


pip install django
pip install pillow
pip install django-leaflet
pip install gdal
pip install geodjango



