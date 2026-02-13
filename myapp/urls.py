from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdminCategoryViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
admin_router = DefaultRouter()
admin_router.register(r"admin/category", AdminCategoryViewSet, basename="admin-category")

urlpatterns = [
    path("", include(router.urls)),
    path("api/v1.0.0/", include(admin_router.urls)),
]
