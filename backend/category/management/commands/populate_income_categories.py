from django.core.management.base import BaseCommand
from category.models import Category

class Command(BaseCommand):
    help = 'Populate built‑in income categories'

    def handle(self, *args, **kwargs):
        # List of default income categories
        built_in_categories = ['Salary', 'Bonus', 'Freelance', 'Investment']

        for cat_name in built_in_categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'type': 'income',
                    'built_in': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created income category: {cat_name}'))
            else:
                self.stdout.write(f'Income category already exists: {cat_name}')