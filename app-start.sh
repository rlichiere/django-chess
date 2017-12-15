
set -e

python manage.py migrate

python manage.py create_superuser -l "$ADMIN_USER" -e "$ADMIN_EMAIL" -p "$ADMIN_PASSWORD"

python manage.py runserver 0.0.0.0:8000
