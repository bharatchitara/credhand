# Deployment Guide

## Production Checklist

- [ ] Update `DEBUG = False` in settings.py
- [ ] Set strong `DJANGO_SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Setup HTTPS/SSL certificates
- [ ] Configure database backup
- [ ] Setup logging
- [ ] Configure email backend
- [ ] Setup static files CDN
- [ ] Configure database replication
- [ ] Setup monitoring and alerts

## Server Requirements

- **OS**: Ubuntu 20.04 LTS or CentOS 8+
- **Python**: 3.8+
- **MySQL**: 8.0+
- **RAM**: Minimum 2GB
- **Storage**: Minimum 20GB

## Deployment Steps

### 1. Server Setup

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3.9 python3-pip python3-venv
sudo apt-get install -y mysql-server nginx
sudo apt-get install -y git supervisor
```

### 2. Clone Repository

```bash
cd /var/www
sudo git clone <repository-url> credhand
sudo chown -R $USER:$USER credhand
cd credhand/backend
```

### 3. Setup Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Create database
mysql -u root -p < ../config/database.sql

# Run migrations
python manage.py migrate
```

### 5. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 6. Create Gunicorn Service

Create `/etc/systemd/system/credhand.service`:

```ini
[Unit]
Description=CredHand Django Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/credhand/backend
ExecStart=/var/www/credhand/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/credhand.sock \
    credhand_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl start credhand
sudo systemctl enable credhand
```

### 7. Nginx Configuration

Create `/etc/nginx/sites-available/credhand`:

```nginx
upstream credhand {
    server unix:/run/credhand.sock;
}

server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/credhand/backend/staticfiles/;
    }

    location /media/ {
        alias /var/www/credhand/backend/media/;
    }

    location / {
        proxy_pass http://credhand;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/credhand /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. SSL Certificate (Let's Encrypt)

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 9. Database Backup

Create `/usr/local/bin/backup-credhand.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backups/credhand"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
mysqldump -u root -p credhand_db > $BACKUP_DIR/credhand_db_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "credhand_db_*.sql" -mtime +7 -delete
```

Schedule with cron:
```bash
0 2 * * * /usr/local/bin/backup-credhand.sh
```

### 10. Monitoring

Install monitoring tools:
```bash
sudo apt-get install -y htop iotop nethogs
```

Setup log monitoring:
```bash
sudo tail -f /var/log/credhand/error.log
```

## Environment Variables for Production

```env
DEBUG=False
DJANGO_SECRET_KEY=your-very-secure-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=credhand_db_prod
DB_USER=credhand_user
DB_PASSWORD=secure-db-password
DB_HOST=localhost
DB_PORT=3306

GOOGLE_OAUTH_CLIENT_ID=prod-client-id
GOOGLE_OAUTH_CLIENT_SECRET=prod-client-secret
GOOGLE_OAUTH_REDIRECT_URI=https://yourdomain.com/auth/callback/

UPI_GATEWAY=razorpay
UPI_KEY_ID=prod-key-id
UPI_KEY_SECRET=prod-key-secret

CORS_ALLOWED_ORIGINS=https://yourdomain.com
FRONTEND_URL=https://yourdomain.com
```

## Performance Optimization

### Database
```bash
# Add indexes
mysql -u root -p credhand_db < /path/to/optimization.sql

# Enable query caching
# Configure in MySQL my.cnf
```

### Caching
```python
# Add to settings.py for production
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
```

### Static Files CDN
Configure CloudFlare or AWS CloudFront for static file delivery.

## Monitoring and Logging

### Application Logs
```bash
# View Django logs
sudo journalctl -u credhand -f
```

### Access Logs
```bash
# View Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

### Performance Metrics
```bash
# Monitor resource usage
htop
```

## Troubleshooting Production Issues

### 500 Error
- Check logs: `sudo journalctl -u credhand -n 50`
- Verify database connection
- Check permissions on files

### Slow Response Time
- Check database queries
- Verify cache is working
- Check CPU/Memory usage

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check Nginx configuration
- Verify file permissions

## Backup and Recovery

### Backup Database
```bash
mysqldump -u root -p credhand_db > backup.sql
```

### Restore Database
```bash
mysql -u root -p credhand_db < backup.sql
```

## Scaling

For high traffic:
1. Use load balancer (HAProxy/Nginx)
2. Multiple Gunicorn workers
3. Database replication
4. Redis for caching
5. CDN for static files
6. Horizontal pod autoscaling (if using Kubernetes)

## Support

For deployment issues, contact DevOps team.
