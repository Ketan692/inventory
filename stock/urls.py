from django.contrib import admin
from django.urls import path, include
from .views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("categories", CategoryViewSet, basename="categories")
router.register("products", ProductViewSet, basename="products")
router.register("suppliers", SupplierViewSet, basename="suppliers")
router.register("stock-transactions", StockTransactionViewSet, basename="stocktransactions")
router.register("customers", CustomerViewSet, basename="customers")
router.register("orders", OrderViewSet, basename="orders")
router.register("order-items", OrderItemViewSet, basename="orderitems")

urlpatterns = [
    path("", include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('analytics/revenue/', total_revenue, name="total_revenue"),
    path('analytics/top-products/', top_products, name="top_products"),
    path("analytics/monthly-sales/", monthly_sales, name="monthly_sales"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(), name="swagger-ui")
]
