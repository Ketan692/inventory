from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .models import *
from .serialisers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category", "supplier")
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        transactions = StockTransaction.objects.filter(product=pk)
        serializer = StockTransactionSerializer(transactions, many=True)

        return Response(serializer.data) 
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        products = Product.objects.filter(stock_lte=5)
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)
    

class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminUser]
    

class StockTransactionViewSet(ModelViewSet):
    queryset = StockTransaction.objects.all()
    serializer_class = StockTransactionSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post']
    

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def complete(self, request, pk=None):

        order = self.get_object()
        order.complete()

        return Response({"message": "Order completed successfully"})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def cancel(self, request, pk=None):

        order = self.get_object()
        order.cancel()

        return Response({"message": "Order cancelled successfully"})

    
class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.select_related("product", "order")
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    

@api_view(['GET'])
@permission_classes([IsAdminUser])
def total_revenue(request):
    revenue = Order.objects.filter(status="COMPLETED").aggregate(total=Sum("total_amount"))

    return Response({
        "Total revenue": revenue["total"] or 0
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def top_products(request):
    products = (
        OrderItem.objects
        .values("product_id", product_name=F("product__name"))
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")
    )

    return Response(products)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def monthly_sales(request):
    sales = (
        Order.objects
        .filter(status="COMPLETED")
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(revenue=Sum("total_amount"))
        .order_by("month")
    )

    return Response(sales)


