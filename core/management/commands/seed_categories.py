from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.utils import seed_default_categories

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed default categories. Pass --user=<username> for one user, or run without args for all users missing categories.'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=str, help='Username to seed categories for.')

    def handle(self, *args, **options):
        username = options.get('user')
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stderr.write(self.style.ERROR(f'User "{username}" not found.'))
                return
            seed_default_categories(user)
            self.stdout.write(self.style.SUCCESS(f'Seeded categories for {user.username}.'))
        else:
            users = User.objects.filter(categories__isnull=True).distinct()
            count = 0
            for user in users:
                seed_default_categories(user)
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Seeded categories for {count} user(s).'))
