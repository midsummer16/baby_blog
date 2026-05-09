from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates admin user if not exists'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Admin user created (admin/admin)'))
        else:
            self.stdout.write('Admin user already exists')
        User.objects.filter(username='admin').update(role='admin')
