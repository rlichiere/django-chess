
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-l', '--login', help="Login", default=None)
        parser.add_argument('-e', '--email', help="Email", default=None)
        parser.add_argument('-p', '--password', help="Password", default=None)

    def handle(self, **options):
        if not options['login'] or not options['email'] or not options['password']:
            print '[CRITICAL] create_superuser: Expecting a login, email and password.'
            exit(1)

        if User.objects.filter(username=options['login']).count() > 0:
            print ('[INFORMATION] create_superuser: Admin already exists.')
        else:
            User.objects.create_superuser(username=options['login'], email=options['email'], password=options['password'])
            print ('[INFORMATION] create_superuser: Admin created.')
