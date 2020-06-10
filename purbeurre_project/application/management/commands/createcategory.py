from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from application.models import Category

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('category_name', type=str, help='Name of the category')
        parser.add_argument('category_url', type=str, help='The category url')

    def handle(self, *args, **options):
        category_name = options['category_name']
        category_url = options['category_url']
        self.create_category(category_name, category_url)

    def create_category(self, category_name, category_url):
        Category.objects.get_or_create(category_name=category_name, category_url=category_url)
        try:
            Category.objects.get_or_create(category_name=category_name, category_url=category_url)
        except IntegrityError as error:
            pass