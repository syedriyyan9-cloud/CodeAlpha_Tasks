from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Menu(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Inventory(models.Model):
    menu_item = models.OneToOneField(Menu, on_delete=models.CASCADE)  # one dish = one stock count
    quantity_available = models.PositiveIntegerField(default=0)  # cannot go negative
    
    def __str__(self):
        return f"{self.menu_item.name} - {self.quantity_available} left"

class Table(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"Table {self.table_number} (seats {self.capacity})"

class Reservation(models.Model):
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.user.username} - Table {self.table.table_number} on {self.date}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(Menu, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    additional_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Order #{self.order.id})"