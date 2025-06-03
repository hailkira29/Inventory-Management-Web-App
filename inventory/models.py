from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.urls import reverse

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=200, unique=True)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
      # Analytics fields
    reorder_level = models.IntegerField(default=10, validators=[MinValueValidator(0)], help_text="Minimum stock level before reordering")
    category = models.CharField(max_length=100, default='General', help_text="Item category")
    supplier = models.CharField(max_length=200, blank=True, null=True, help_text="Supplier name")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Get URL for item detail view"""
        from django.urls import reverse
        return reverse('inventory:item_detail', kwargs={'pk': self.pk})
    
    @property
    def total_value(self):
        """Calculate total value (quantity * price)"""
        return self.quantity * self.price
    
    @property
    def is_low_stock(self):
        """Check if item is below reorder level"""
        return self.quantity <= self.reorder_level
    
    @property
    def is_out_of_stock(self):
        """Check if item is out of stock"""
        return self.quantity == 0
    
    @property
    def stock_status(self):
        """Get stock status"""
        if self.quantity == 0:
            return 'Out of Stock'
        elif self.is_low_stock:
            return 'Low Stock'
        else:
            return 'In Stock'
    
    def update_stock(self, quantity_change, transaction_type, reason="", user=None):
        """Update stock and create transaction record"""
        old_quantity = self.quantity
        self.quantity += quantity_change
        if self.quantity < 0:
            raise ValueError("Stock cannot be negative")
        self.save()
        
        # Create transaction record
        InventoryTransaction.objects.create(
            item=self,
            transaction_type=transaction_type,
            quantity=abs(quantity_change),
            reason=reason,
            user=user
        )
        
        # Check for alerts
        self.check_and_create_alerts()
        
        return self.quantity
    
    def check_and_create_alerts(self):
        """Check stock levels and create alerts if needed"""
        # Remove existing unresolved alerts for this item
        InventoryAlert.objects.filter(item=self, is_resolved=False).delete()
        
        if self.quantity == 0:
            InventoryAlert.objects.create(
                item=self,
                alert_type='OUT_OF_STOCK',
                message=f'Item "{self.name}" is out of stock. Immediate restocking required.'
            )
        elif self.is_low_stock:
            InventoryAlert.objects.create(
                item=self,
                alert_type='LOW_STOCK',
                message=f'Item "{self.name}" is running low. Current stock: {self.quantity}, Reorder level: {self.reorder_level}'
            )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'


class InventoryTransaction(models.Model):
    """Track inventory movements for analytics"""
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJUST', 'Adjustment'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.item.name} - {self.transaction_type} ({self.quantity})"
    
    class Meta:
        ordering = ['-timestamp']


class InventoryAlert(models.Model):
    """System alerts for inventory management"""
    ALERT_TYPES = [
        ('LOW_STOCK', 'Low Stock'),
        ('OUT_OF_STOCK', 'Out of Stock'),
        ('OVERSTOCK', 'Overstock'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.alert_type}: {self.item.name}"
    
    def resolve(self):
        """Mark alert as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.save()
    
    class Meta:
        ordering = ['-created_at']
