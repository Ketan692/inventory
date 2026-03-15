from django.db import models, transaction
from base.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError


class Category(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    
class Supplier(BaseModel):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True,blank=True, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class StockTransaction(BaseModel):
    TRANSACTION_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJUST', 'Adjustment')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    note = models.TextField(null=True, blank=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.transaction_type == 'IN':
                self.product.stock += self.quantity
            elif self.transaction_type == 'OUT':
                if self.product.stock < self.quantity:
                    raise ValidationError('Not enough stock available.')
                self.product.stock -= self.quantity
            elif self.transaction_type == 'ADJUST':
                self.product.stock = self.quantity

            self.product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.transaction_type} - {self.quantity}"
    

class Customer(BaseModel):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Order(BaseModel):
    ORDER_STATUS = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='PENDING'
    )
    
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"

    @transaction.atomic
    def cancel(self):
        if self.status == "CANCELLED":
            raise ValidationError("Order is already cancelled.")
        if self.status == "COMPLETED":
            raise ValidationError("Completed order cannot be cancelled.")
        
        for item in self.items.all():

            StockTransaction.objects.create(
                product = item.product,
                transaction_type = "IN",
                quantity = item.quantity,
                note = f"Order #{self.id} cancelled."
            )
        self.status = "CANCELLED"
        self.total_amount = 0
        self.save()

    def complete(self):
        if self.status !="PENDING":
            raise ValidationError("Only pending orders can be completed.")
        if not self.items.exists():
            raise ValidationError("cannot complete order without items.")
        
        self.status = "COMPLETED"
        self.save()
    

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Order items cannot be modified.")

        if self.order.status != "PENDING":
            raise ValidationError("Items can only be added to PENDING orders.")
        
        if not self.pk:
            self.price = self.product.price
            if self.product.stock < self.quantity:
                raise ValidationError("Not enough stock available.")
            

            StockTransaction.objects.create(
                product=self.product,
                transaction_type="OUT",
                quantity=self.quantity,
                note=f"Order #{self.order.id}"
            )

            self.order.total_amount += self.price * self.quantity
            self.order.save()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"