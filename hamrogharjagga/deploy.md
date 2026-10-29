# HamroGhajagga — Production Deployment Guide

This guide provides end-to-end instructions for deploying the **HamroGhajagga** (Nepal Real Estate & Land Management Platform) on a Linux Virtual Private Server (Ubuntu 22.04 / 24.04 LTS), Docker, or PaaS providers (Render, Railway, DigitalOcean).

---

## 1. System Requirements & Architecture

- **Operating System**: Ubuntu 22.04 LTS or 24.04 LTS
- **Python**: 3.11, 3.12, or 3.13
- **Database**: PostgreSQL 15+ (recommended for production) or SQLite (for demo/small instances)
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
   [ PostgreSQL / SQLite Database ]
```

---

## 2. Server Initial Setup & Dependencies

Connect to your Ubuntu server via SSH and update packages:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl git
```

---

## 3. PostgreSQL Database Setup

```bash
sudo -u postgres psql
```

Inside PostgreSQL shell:

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

## 4. Clone Project & Set Up Virtual Environment

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

## 5. Production Environment Variables Configuration

Create a `.env` file in the project root:

```bash
nano /var/www/hamrogharjagga/.env
```

Add the following environment settings:

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

## 6. Run Migrations & Collect Static Files

```bash
# Apply all database migrations
python manage.py migrate

# Create initial Superuser (Admin)
python manage.py createsuperuser

# Collect static assets into staticfiles/ directory
python manage.py collectstatic --noinput

# Set appropriate permissions for uploaded media files
mkdir -p media
sudo chown -R www-data:www-data media
sudo chmod -R 775 media
```

---

## 7. Gunicorn Systemd Service Configuration

Create a systemd service file for Gunicorn:

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

Create log folder, enable and start Gunicorn:

```bash
sudo mkdir -p /var/log/gunicorn
sudo systemctl daemon-reload
sudo systemctl start hamrogharjagga
sudo systemctl enable hamrogharjagga
sudo systemctl status hamrogharjagga
```

---

## 8. Nginx Reverse Proxy Configuration

Create an Nginx configuration file:

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

    # Proxy all other requests to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/hamrogharjagga /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 9. SSL Certificate Setup (Let's Encrypt HTTPS)

Secure your deployment with free SSL via Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot will automatically reconfigure Nginx for HTTPS on port 443 and setup certificate auto-renewal.

---

## 10. Platform Health Verification

Verify that all services are operational:

1. **Web Access**: Navigate to `https://yourdomain.com/` — The home page should load cleanly with featured land properties.
2. **Admin Portal**: Navigate to `https://yourdomain.com/admin/` — Log in with the superuser credentials.
3. **Interactive Search**: Visit `https://yourdomain.com/buyer/find_land/` — Check the Leaflet map and area filters.
4. **API Endpoints**: Check live JSON responses:
   - `GET /api/properties/`
   - `GET /api/stats/`

---

## 11. Maintenance & Routine Commands

```bash
# Check service status
sudo systemctl status hamrogharjagga

# Restart application after pulling updates
cd /var/www/hamrogharjagga
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart hamrogharjagga

# View live application logs
sudo journalctl -u hamrogharjagga -f
```
