from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Deletes all superusers from the database'

    def handle(self, *args, **options):
        count = User.objects.filter(is_superuser=True).count()
        User.objects.filter(is_superuser=True).delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} superusers')) 