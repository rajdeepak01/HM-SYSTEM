# HM-SYSTEM
Hospital Management System

System for Managing Hospitals

Project File structure is like:

# Frontend

# Backend

### Activate virtual enviroment: 
source .env/bin/activate

### Creating virtual enviroment
python3 -m venv .env

### run celery worker
<!-- celery -A app.celery worker --loglevel=info -->
celery -A app.celery worker --beat --loglevel=info
### run redis server
redis-server

## run smtp server
python -m aiosmtpd -n -l localhost:1025