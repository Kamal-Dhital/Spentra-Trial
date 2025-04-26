from rest_framework import viewsets
from .models import Budget
from .serializers import BudgetSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all().order_by('year', 'month')
    serializer_class = BudgetSerializer