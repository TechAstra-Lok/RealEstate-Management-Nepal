# HamroGhajagga — Deployment & Setup Guide

This comprehensive guide covers both **Local Deployment** (for local development, testing, and demonstration on Windows, macOS, and Linux) and **Production Deployment** (for deploying to an Ubuntu VPS with Nginx, Gunicorn, PostgreSQL, and SSL).

---

# Part 1: Local Deployment (Windows, macOS, Linux)

Follow these steps to run **HamroGhajagga** on your local machine for development or testing.

### 1.1 Prerequisites
- **Python**: Version 3.11, 3.12, or 3.13 installed.
  - Verify with: `python --version` (or `python3 --version`)
- **Git**: Installed and available in PATH.
  - Verify with: `git --version`

---

### 1.2 Clone the Repository
Open your terminal (PowerShell, Command Prompt, or Bash) and clone the repository:

```bash
git clone https://github.com/TechAstra-Lok/RealEstate-Management-Nepal.git hamrogharjagga
cd hamrogharjagga
```

---

### 1.3 Create and Activate a Virtual Environment

#### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
> *Note for PowerShell users*: If you see an execution policy error, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` and try activating again.

#### On Windows (Command Prompt):
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 1.4 Install Dependencies
Ensure `pip` is up to date, then install all project dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 1.5 Database Setup & Superuser Creation

The platform uses SQLite by default for local development (no external database server required):

```bash
# 1. Apply database migrations
python manage.py migrate

# 2. (Optional) Create an administrative superuser to access the Django Admin
python manage.py createsuperuser
```
Follow the interactive prompts to set an email, full name, and password.

---

### 1.6 Run the Local Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You should see output similar to:
```text
Django version 5.1.5, using settings 'hamrogharjagga.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

To run on a specific port or make it accessible to your local network:
```bash
python manage.py runserver 0.0.0.0:8000
```

---

### 1.7 Local URLs Reference

Once the server is running, open your browser and navigate to:

| Page / Feature | Local URL | Description |
|---|---|---|
| **Home Page** | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | Hero section, featured properties, role-based login/signup modals. |
| **Buyer Property Search** | [http://127.0.0.1:8000/buyer/find_land/](http://127.0.0.1:8000/buyer/find_land/) | Interactive Leaflet map, multi-unit land area filters, and sorting. |
| **Buyer Wishlist** | [http://127.0.0.1:8000/buyer/wishlist/](http://127.0.0.1:8000/buyer/wishlist/) | Buyer's saved properties list. |
| **Seller Dashboard** | [http://127.0.0.1:8000/seller/dashboard/](http://127.0.0.1:8000/seller/dashboard/) | Analytics, chart metrics, inquiries feed, and property listings. |
| **List New Property** | [http://127.0.0.1:8000/seller/sell/](http://127.0.0.1:8000/seller/sell/) | Interactive pin drop map, media uploads, and listing form. |
| **Seller Listings** | [http://127.0.0.1:8000/seller/my-properties/](http://127.0.0.1:8000/seller/my-properties/) | Paginated list of properties owned by the seller. |
| **Django Admin** | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) | Back-office management for users, properties, inlines, and inquiries. |
| **REST API Properties** | [http://127.0.0.1:8000/api/properties/](http://127.0.0.1:8000/api/properties/) | Real-time JSON listings & geospatial coordinates endpoint. |
| **REST API Live Stats** | [http://127.0.0.1:8000/api/stats/](http://127.0.0.1:8000/api/stats/) | Platform live metrics. |

---

### 1.8 Common Local Issues & Troubleshooting

- **Port 8000 already in use**:
  Run on an alternative port: `python manage.py runserver 8080`.
- **Media Uploads**:
  Uploaded property images and videos are stored in `hamrogharjagga/media/`. Django automatically serves them in `DEBUG = True` mode.
- **System Check**:
  Verify your local environment at any time by running:
  ```bash
  python manage.py check
  ```
  *(Should output: `System check identified no issues (0 silenced)`)*

---

# Part 2: Production Deployment (Ubuntu VPS, Nginx, Gunicorn, PostgreSQL, SSL)

This section provides end-to-end instructions for deploying to a production server (Ubuntu 22.04 LTS / 24.04 LTS).

### 2.1 System Requirements & Architecture

- **Operating System**: Ubuntu 22.04 LTS or 24.04 LTS
- **Python**: 3.11+
- **Database**: PostgreSQL 15+
- **Web Server**: Nginx (Reverse Proxy + Static File Serving + SSL)
- **WSGI Server**: Gunicorn 23.x
- **Process Manager**: Systemd

```
[ Client / Browser ] 
        │
   HTTPS (Port 443)
        ▼
   [ Nginx Reverse Proxy ]
   ├── Serves /static/ directly from /var/www/hamrogharjagga/staticfiles/
   ├── Serves /media/ directly from /var/www/hamrogharjagga/media/
   └── Proxies API & Dynamic Requests to http://127.0.0.1:8000
        ▼
   [ Gunicorn WSGI ]
        ▼
   [ Django Application (hamrogharjagga.wsgi) ]
        ▼
   [ PostgreSQL Database ]
```

---

### 2.2 Server Initial Setup & Packages

Connect to your Ubuntu server via SSH and install the system prerequisites:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl git
```

---

### 2.3 PostgreSQL Database Setup

Log into PostgreSQL and create the production database and user:

```bash
sudo -u postgres psql
```

Inside the PostgreSQL shell:

```sql
CREATE DATABASE hamrogharjagga_db;
CREATE USER hamro_user WITH PASSWORD 'YourStrongSecurePassword123!';
ALTER ROLE hamro_user SET client_encoding TO 'utf8';
ALTER ROLE hamro_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE hamro_user SET timezone TO 'Asia/Kathmandu';
GRANT ALL PRIVILEGES ON DATABASE hamrogharjagga_db TO hamro_user;
\q
```

---

### 2.4 Clone Project & Set Up Production Virtual Environment

```bash
# Clone the repository
cd /var/www
sudo git clone https://github.com/TechAstra-Lok/RealEstate-Management-Nepal.git hamrogharjagga
sudo chown -R $USER:$USER /var/www/hamrogharjagga
cd /var/www/hamrogharjagga

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install production dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 2.5 Production Environment Variables Configuration

Create a production `.env` file:

```bash
nano /var/www/hamrogharjagga/.env
```

Add your production configuration:

```ini
DEBUG=False
SECRET_KEY=generate-a-strong-random-50-character-string-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,127.0.0.1

# Database Configuration (PostgreSQL)
DATABASE_URL=postgres://hamro_user:YourStrongSecurePassword123!@localhost:5432/hamrogharjagga_db

# Security Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

---

### 2.6 Run Migrations & Collect Static Files

```bash
# Apply database migrations
python manage.py migrate

# Create the Admin Superuser
python manage.py createsuperuser

# Collect static assets into staticfiles/
python manage.py collectstatic --noinput

# Set permissions for media uploads folder
mkdir -p media
sudo chown -R www-data:www-data media
sudo chmod -R 775 media
```

---

### 2.7 Gunicorn Systemd Service Configuration

Create a systemd unit file for Gunicorn:

```bash
sudo nano /etc/systemd/system/hamrogharjagga.service
```

Paste the following configuration:

```ini
[Unit]
Description=Gunicorn daemon for HamroGhajagga
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/hamrogharjagga
ExecStart=/var/www/hamrogharjagga/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          --access-logfile /var/log/gunicorn/access.log \
          --error-logfile /var/log/gunicorn/error.log \
          hamrogharjagga.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo mkdir -p /var/log/gunicorn
sudo systemctl daemon-reload
sudo systemctl start hamrogharjagga
sudo systemctl enable hamrogharjagga
sudo systemctl status hamrogharjagga
```

---

### 2.8 Nginx Reverse Proxy Configuration

Create an Nginx server configuration:

```bash
sudo nano /etc/nginx/sites-available/hamrogharjagga
```

Paste the configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 50M;

    # Static assets
    location /static/ {
        alias /var/www/hamrogharjagga/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    # Uploaded media (property photos & videos)
    location /media/ {
        alias /var/www/hamrogharjagga/media/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    # Proxy application requests to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration and reload Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/hamrogharjagga /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### 2.9 SSL Certificate Setup (Let's Encrypt HTTPS)

Obtain and configure free SSL with Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot automatically configures HTTPS port 443 in Nginx and installs a renewal cron job.

---

### 2.10 Maintenance & Update Runbook

When deploying updates from the repository:

```bash
cd /var/www/hamrogharjagga
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart hamrogharjagga

# Monitor live application logs
sudo journalctl -u hamrogharjagga -f
```
