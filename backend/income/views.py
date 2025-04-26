from rest_framework import viewsets
from .models import Income
from .serializers import IncomeSerializer

class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all().order_by('-date')
    serializer_class = IncomeSerializer