# Przewodnik Deployment - Ulga na VPS

## Przygotowanie VPS

### 1. Aktualizacja systemu i instalacja zależności
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git nginx -y
```

### 2. Utworzenie użytkownika (jeśli używasz root)
```bash
# Opcjonalnie - lepiej mieć dedykowanego użytkownika
sudo adduser ulga
sudo usermod -aG sudo ulga
su - ulga
```

### 3. Przygotowanie katalogów
```bash
sudo mkdir -p /var/www/ulga
sudo chown -R $USER:$USER /var/www/ulga
cd /var/www/ulga
```

## Instalacja projektu

### 1. Sklonowanie repozytorium
```bash
# Jeśli masz projekt na GitHub
git clone https://github.com/keybipl/ulga.git .

# LUB skopiuj pliki przez SFTP/SCP z Windows:
# scp -r c:\Users\Krzysztof\django\ulga user@vps-ip:/var/www/ulga
```

### 2. Utworzenie wirtualnego środowiska
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalacja zależności
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Konfiguracja zmiennych środowiskowych
```bash
cp .env.example .env
nano .env
```

Edytuj `.env`:
```
SECRET_KEY=WYGENERUJ_NOWY_DŁUGI_KLUCZ
DEBUG=False
ALLOWED_HOSTS=twoja-domena.pl,www.twoja-domena.pl
```

Wygeneruj SECRET_KEY:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Migracje bazy danych
```bash
# Użyj settings_prod dla produkcji
export DJANGO_SETTINGS_MODULE=psi.settings_prod
python manage.py migrate
python manage.py collectstatic --noinput
```

### 6. Utworzenie superusera (opcjonalnie)
```bash
python manage.py createsuperuser
```

### 7. Utworzenie katalogów dla logów
```bash
mkdir -p logs
touch logs/django.log
```

## Konfiguracja Gunicorn i Systemd

### 1. Edycja pliku service
```bash
sudo nano deploy/ulga.service
```

Zmień:
- `User` i `Group` na swojego użytkownika (np. `ulga` lub `www-data`)
- Ścieżki `/var/www/ulga` jeśli instalujesz gdzie indziej

### 2. Instalacja service
```bash
sudo cp deploy/ulga.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ulga
sudo systemctl start ulga
sudo systemctl status ulga
```

### Sprawdzenie logów gunicorn:
```bash
sudo journalctl -u ulga -f
tail -f /var/log/ulga/gunicorn-error.log
```

## Konfiguracja Nginx

### 1. Edycja konfiguracji
```bash
sudo nano deploy/nginx.conf
```

Zmień `server_name` na swoją domenę.

### 2. Instalacja konfiguracji
```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/ulga
sudo ln -s /etc/nginx/sites-available/ulga /etc/nginx/sites-enabled/
```

### 3. Test konfiguracji
```bash
sudo nginx -t
```

### 4. Restart Nginx
```bash
sudo systemctl restart nginx
sudo systemctl status nginx
```

## SSL Certificate (HTTPS)

### Instalacja Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Uzyskanie certyfikatu
```bash
sudo certbot --nginx -d twoja-domena.pl -d www.twoja-domena.pl
```

Certbot automatycznie zaktualizuje konfigurację Nginx.

## Aktualizacja aplikacji

Stwórz skrypt do łatwej aktualizacji:

```bash
nano /var/www/ulga/deploy/update.sh
```

```bash
#!/bin/bash
cd /var/www/ulga
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=psi.settings_prod
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart ulga
echo "Deployment completed!"
```

```bash
chmod +x deploy/update.sh
```

Użycie:
```bash
./deploy/update.sh
```

## Przydatne komendy

### Sprawdzanie statusu
```bash
sudo systemctl status ulga
sudo systemctl status nginx
```

### Restart serwisów
```bash
sudo systemctl restart ulga
sudo systemctl restart nginx
```

### Logi
```bash
# Logi gunicorn
sudo journalctl -u ulga -f
tail -f /var/log/ulga/gunicorn-error.log

# Logi nginx
tail -f /var/log/nginx/ulga-error.log
tail -f /var/log/nginx/ulga-access.log

# Logi Django
tail -f /var/www/ulga/logs/django.log
```

### Backup bazy danych SQLite
```bash
cp /var/www/ulga/db.sqlite3 /var/www/ulga/backups/db_$(date +%Y%m%d_%H%M%S).sqlite3
```

## Rozwiązywanie problemów

### Problem: Gunicorn nie startuje
```bash
# Sprawdź logi
sudo journalctl -u ulga -n 50
# Sprawdź uprawnienia
ls -la /var/www/ulga
# Uruchom gunicorn ręcznie do testów
cd /var/www/ulga
source venv/bin/activate
gunicorn --config deploy/gunicorn_config.py psi.wsgi:application
```

### Problem: 502 Bad Gateway
- Sprawdź czy gunicorn działa: `sudo systemctl status ulga`
- Sprawdź uprawnienia do socketu: `ls -la /var/run/ulga/`
- Sprawdź logi nginx: `tail -f /var/log/nginx/ulga-error.log`

### Problem: Static files nie ładują się
```bash
# Sprawdź czy collectstatic został wykonany
python manage.py collectstatic --noinput
# Sprawdź uprawnienia
sudo chown -R www-data:www-data /var/www/ulga/staticfiles
# Sprawdź konfigurację nginx
sudo nginx -t
```

## Monitoring (opcjonalnie)

### Instalacja htop
```bash
sudo apt install htop
htop
```

### Ustawienie cron do backupów
```bash
crontab -e
```

Dodaj:
```
0 2 * * * cp /var/www/ulga/db.sqlite3 /var/www/ulga/backups/db_$(date +\%Y\%m\%d).sqlite3
```

## Bezpieczeństwo

1. **Firewall (ufw)**:
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

2. **Fail2ban** (opcjonalnie):
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

3. **Regularne aktualizacje**:
```bash
sudo apt update && sudo apt upgrade -y
```

---

Powodzenia z deploymentem! 🚀
