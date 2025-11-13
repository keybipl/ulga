# Konfiguracja VPS dla ulga-psi.pl

## Krok 1: Konfiguracja DNS (u rejestratora domeny)

Zaloguj się do panelu rejestratora domeny (np. OVH, home.pl, nazwa.pl) i ustaw:

```
Typ: A     Host: @              Wartość: 51.89.22.3
Typ: A     Host: www            Wartość: 51.89.22.3
```

**Uwaga:** Propagacja DNS może zająć do 24h (często 1-2h)

---

## Krok 2: Aktualizacja pliku .env na VPS

Połącz się z VPS:
```bash
ssh ubuntu@51.89.22.3
```

Edytuj plik .env:
```bash
nano /home/ubuntu/ulga/.env
```

Zmień zawartość na:
```bash
DJANGO_SETTINGS_MODULE=psi.settings
SECRET_KEY=twoj-bezpieczny-klucz-produkcyjny-min-50-znakow
DEBUG=False
ALLOWED_HOSTS=ulga-psi.pl,www.ulga-psi.pl,51.89.22.3
```

Zapisz: `Ctrl+O`, Enter, `Ctrl+X`

---

## Krok 3: Konfiguracja Nginx z domeną

Utwórz konfigurację Nginx:
```bash
sudo nano /etc/nginx/sites-available/ulga
```

Wklej (zmień na swoją domenę):
```nginx
server {
    listen 80;
    server_name ulga-psi.pl www.ulga-psi.pl;
    
    client_max_body_size 20M;
    
    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        alias /home/ubuntu/ulga/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /home/ubuntu/ulga/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Zapisz i wyjdź.

Aktywuj konfigurację:
```bash
sudo ln -sf /etc/nginx/sites-available/ulga /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Krok 4: Zbierz pliki statyczne Django

```bash
cd /home/ubuntu/ulga
source venv/bin/activate
python manage.py collectstatic --no-input
```

---

## Krok 5: Restart usług

```bash
sudo systemctl restart ulga
sudo systemctl status ulga
```

---

## Krok 6: Instalacja certyfikatu SSL (HTTPS)

Po propagacji DNS (1-24h), zainstaluj certyfikat Let's Encrypt:

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y

sudo certbot --nginx -d ulga-psi.pl -d www.ulga-psi.pl
```

Postępuj zgodnie z instrukcjami:
- Podaj swój email
- Zaakceptuj regulamin (Y)
- Wybierz przekierowanie HTTP → HTTPS (opcja 2)

Certbot automatycznie skonfiguruje HTTPS i auto-renewal.

---

## Krok 7: Testowanie

Sprawdź czy działa:
```bash
# Test lokalny na VPS
curl -I http://localhost:8000

# Test przez domenę (po propagacji DNS)
curl -I http://ulga-psi.pl
```

Otwórz w przeglądarce:
- http://ulga-psi.pl (po propagacji DNS)
- https://ulga-psi.pl (po certyfikacie SSL)

---

## Rozwiązywanie problemów

### Problem: 502 Bad Gateway
```bash
# Sprawdź status gunicorn
sudo systemctl status ulga

# Sprawdź logi
sudo journalctl -u ulga -n 50
```

### Problem: CSS nie działa
```bash
# Sprawdź uprawnienia
sudo chown -R ubuntu:ubuntu /home/ubuntu/ulga/staticfiles
sudo chmod -R 755 /home/ubuntu/ulga/staticfiles

# Ponownie zbierz pliki statyczne
cd /home/ubuntu/ulga
source venv/bin/activate
python manage.py collectstatic --no-input --clear
```

### Problem: Domena nie działa
```bash
# Sprawdź propagację DNS
nslookup ulga-psi.pl
dig ulga-psi.pl

# Sprawdź konfigurację Nginx
sudo nginx -t
sudo systemctl status nginx
```

### Logi Nginx
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

---

## Automatyczne odnowienie certyfikatu SSL

Certbot automatycznie konfiguruje cron job. Sprawdź:
```bash
sudo systemctl status certbot.timer
```

Test odnowienia:
```bash
sudo certbot renew --dry-run
```

---

## Checklist końcowy

- [ ] DNS skonfigurowane (A records)
- [ ] .env zaktualizowany (ALLOWED_HOSTS z domeną)
- [ ] Nginx skonfigurowany
- [ ] Static files zebrane
- [ ] Gunicorn działa
- [ ] Nginx działa
- [ ] Strona działa na http://ulga-psi.pl
- [ ] SSL certyfikat zainstalowany
- [ ] Strona działa na https://ulga-psi.pl
- [ ] Auto-renewal SSL skonfigurowane

---

## Przydatne komendy

```bash
# Status wszystkich usług
sudo systemctl status ulga nginx

# Restart wszystkiego
sudo systemctl restart ulga nginx

# Logi live
sudo journalctl -u ulga -f

# Test konfiguracji
sudo nginx -t

# Sprawdź, czy port 8000 jest otwarty
sudo netstat -tlnp | grep 8000
```

---

## Bezpieczeństwo po wdrożeniu

1. **Firewall** (jeśli nie skonfigurowany):
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

2. **Zmień SECRET_KEY** w .env na długi, losowy ciąg

3. **Backup bazy danych** (regularnie):
```bash
# Backup
cp /home/ubuntu/ulga/db.sqlite3 /home/ubuntu/backups/db_$(date +%Y%m%d).sqlite3

# Lub ustaw cron job
crontab -e
# Dodaj linię:
0 3 * * * cp /home/ubuntu/ulga/db.sqlite3 /home/ubuntu/backups/db_$(date +\%Y\%m\%d).sqlite3
```

---

## Kontakt w razie problemów

Jeśli coś nie działa:
1. Sprawdź logi: `sudo journalctl -u ulga -n 100`
2. Sprawdź Nginx: `sudo nginx -t && sudo tail /var/log/nginx/error.log`
3. Sprawdź DNS: `nslookup ulga-psi.pl`
