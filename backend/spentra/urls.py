from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib import admin

schema_view = get_schema_view(
    openapi.Info(
        title="Authentication API",
        default_version='v1',
        description="API documentation for authentication endpoints.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/income/', include('income.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/budgeting/', include('budgeting.urls')),
]