from django.db import models

class Category(models.Model):
    CATEGORY_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('budget', 'Budget'),
        ('transaction', 'Transaction'),
    )
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    built_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.type})"