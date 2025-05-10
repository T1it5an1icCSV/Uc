import os
import sys
import sqlite3
import django

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection

# Удаляем старую базу данных
try:
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("База данных успешно удалена")
except Exception as e:
    print(f"Ошибка при удалении базы данных: {e}")
    
# Выполняем миграции
os.system('python manage.py migrate')

# Создаем суперпользователя, если не существует
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print("Суперпользователь admin создан (пароль: admin)")
except Exception as e:
    print(f"Ошибка при создании суперпользователя: {e}")

print("База данных успешно пересоздана!") 