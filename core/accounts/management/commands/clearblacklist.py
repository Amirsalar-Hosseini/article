from django.core.management.base import BaseCommand
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


class Command(BaseCommand):
    help = 'Clear all entries from the token blacklist'

    def handle(self, *args, **options):
        BlacklistedToken.objects.all().delete()
        OutstandingToken.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully cleared all blacklisted tokens.'))
