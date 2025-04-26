from rest_framework import viewsets
from category.models import Category
from category.serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('type', 'name')
    serializer_class = CategorySerializer