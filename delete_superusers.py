import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

# Delete all superusers
User.objects.filter(is_superuser=True).delete()
print("All superusers have been deleted successfully.") 