from django.db import models

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("income", "Income"),
        ("expense", "Expense"),
    )
    title = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title