from django.db import models

class Budget(models.Model):
    category = models.CharField(max_length=50)
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.category} - {self.month}/{self.year}"