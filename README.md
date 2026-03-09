# HM-SYSTEM — Hospital Management System

> A comprehensive system for managing hospital operations.


##  Getting Started

### 1. Create Virtual Environment
python3 -m venv .env

### 2. Activate Virtual Environment
source .env/bin/activate

## Running Services

### Celery Worker

1) celery -A app.celery worker --loglevel=info

2)  
### Redis Server

redis-server

### 📧 SMTP Server (Development)

python -m aiosmtpd -n -l localhost:1025

### MailHog
mailhog
