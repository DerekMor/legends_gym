from django.db import models
from profiles.models import Customer
from products.models import Product
import uuid
from django.contrib.auth.models import User

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=32, null=False, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)

    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, blank=True, null=True)

    def _generate_order_number(self):

        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):

        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    def apply_discount_code(self, discount_code):
        try:
            code = DiscountCode.objects.get(code=discount_code, is_active=True, used=False)
            discount_amount = (code.percentage / 100) * self.order_total
            self.order_total -= discount_amount
            
            code.used = True
            code.save()
            self.save()
        except DiscountCode.DoesNotExist:
            raise ValidationError("Invalid or used discount code.")


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):

        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.order.order_number} - Product {self.product.name}'

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Order History"

