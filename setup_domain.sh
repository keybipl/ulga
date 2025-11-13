#!/bin/bash
# Skrypt konfiguracji domeny ulga-psi.pl na VPS
# Uruchom na serwerze jako: bash setup_domain.sh

echo "=========================================="
echo "Konfiguracja domeny ulga-psi.pl"
echo "=========================================="

# Kolory
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Sprawdź czy jesteś na VPS
if [ ! -d "/home/ubuntu/ulga" ]; then
    echo -e "${RED}Błąd: Katalog /home/ubuntu/ulga nie istnieje!${NC}"
    echo "Ten skrypt należy uruchomić na serwerze VPS."
    exit 1
fi

# Krok 1: Aktualizacja .env
echo -e "\n${YELLOW}Krok 1: Aktualizacja pliku .env${NC}"
echo "Obecna zawartość ALLOWED_HOSTS:"
grep ALLOWED_HOSTS /home/ubuntu/ulga/.env

echo -e "\n${GREEN}Czy zaktualizować ALLOWED_HOSTS na: ulga-psi.pl,www.ulga-psi.pl,51.89.22.3?${NC}"
read -p "Kontynuować? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Backup .env
    cp /home/ubuntu/ulga/.env /home/ubuntu/ulga/.env.backup_$(date +%Y%m%d_%H%M%S)
    
    # Aktualizuj ALLOWED_HOSTS
    sed -i 's/^ALLOWED_HOSTS=.*/ALLOWED_HOSTS=ulga-psi.pl,www.ulga-psi.pl,51.89.22.3/' /home/ubuntu/ulga/.env
    echo -e "${GREEN}✓ Zaktualizowano .env${NC}"
fi

# Krok 2: Konfiguracja Nginx
echo -e "\n${YELLOW}Krok 2: Konfiguracja Nginx${NC}"

if [ -f "/etc/nginx/sites-available/ulga" ]; then
    echo -e "${YELLOW}Plik konfiguracyjny już istnieje. Tworzę backup...${NC}"
    sudo cp /etc/nginx/sites-available/ulga /etc/nginx/sites-available/ulga.backup_$(date +%Y%m%d_%H%M%S)
fi

echo "Tworzę konfigurację Nginx..."
sudo tee /etc/nginx/sites-available/ulga > /dev/null <<'EOF'
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
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

# Aktywuj konfigurację
sudo ln -sf /etc/nginx/sites-available/ulga /etc/nginx/sites-enabled/
echo -e "${GREEN}✓ Konfiguracja Nginx utworzona${NC}"

# Test konfiguracji Nginx
echo -e "\n${YELLOW}Testowanie konfiguracji Nginx...${NC}"
if sudo nginx -t; then
    echo -e "${GREEN}✓ Konfiguracja Nginx poprawna${NC}"
else
    echo -e "${RED}✗ Błąd w konfiguracji Nginx!${NC}"
    exit 1
fi

# Krok 3: Zbieranie plików statycznych
echo -e "\n${YELLOW}Krok 3: Zbieranie plików statycznych${NC}"
cd /home/ubuntu/ulga
source venv/bin/activate
python manage.py collectstatic --no-input
echo -e "${GREEN}✓ Pliki statyczne zebrane${NC}"

# Krok 4: Restart usług
echo -e "\n${YELLOW}Krok 4: Restart usług${NC}"
sudo systemctl restart ulga
sleep 2
sudo systemctl reload nginx

# Sprawdź status
if sudo systemctl is-active --quiet ulga; then
    echo -e "${GREEN}✓ Usługa ulga działa${NC}"
else
    echo -e "${RED}✗ Usługa ulga nie działa!${NC}"
    sudo systemctl status ulga
    exit 1
fi

if sudo systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx działa${NC}"
else
    echo -e "${RED}✗ Nginx nie działa!${NC}"
    sudo systemctl status nginx
    exit 1
fi

# Podsumowanie
echo -e "\n${GREEN}=========================================="
echo "✓ Konfiguracja zakończona!"
echo "==========================================${NC}"
echo ""
echo "Następne kroki:"
echo "1. Upewnij się, że DNS jest skonfigurowane:"
echo "   A record: ulga-psi.pl → 51.89.22.3"
echo "   A record: www.ulga-psi.pl → 51.89.22.3"
echo ""
echo "2. Po propagacji DNS (1-24h), zainstaluj SSL:"
echo "   sudo certbot --nginx -d ulga-psi.pl -d www.ulga-psi.pl"
echo ""
echo "3. Testuj:"
echo "   curl -I http://ulga-psi.pl"
echo ""
echo "Status usług:"
sudo systemctl status ulga --no-pager | head -3
sudo systemctl status nginx --no-pager | head -3
