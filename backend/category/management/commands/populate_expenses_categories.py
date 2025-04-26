from django.core.management.base import BaseCommand
from category.models import Category

class Command(BaseCommand):
    help = 'Populate built‑in expense categories'

    def handle(self, *args, **kwargs):
        # List of default expense categories
        built_in_categories = ['Home', 'School', 'Food', 'Transport', 'Entertainment']

        for cat_name in built_in_categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'type': 'expense',
                    'built_in': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))
            else:
                self.stdout.write(f'Category already exists: {cat_name}')