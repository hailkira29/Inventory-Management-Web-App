from django.contrib import admin
from .models import Item, InventoryTransaction, InventoryAlert

# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'price', 'category', 'supplier', 'get_stock_status', 'get_total_value', 'created_at']
    list_filter = ['category', 'supplier', 'created_at', 'updated_at']
    search_fields = ['name', 'category', 'supplier']
    ordering = ['name']    
    readonly_fields = ['get_total_value', 'get_stock_status', 'created_at', 'updated_at']
    list_per_page = 25
    actions = ['mark_low_stock_items', 'update_reorder_level']
    
    def get_stock_status(self, obj):
        """Display stock status for admin"""
        return obj.stock_status
    get_stock_status.short_description = 'Stock Status'
    
    def get_total_value(self, obj):
        """Display total value for admin"""
        return f"${obj.total_value:,.2f}"
    get_total_value.short_description = 'Total Value'
    
    def get_queryset(self, request):
        """Optimize queryset for admin"""
        return super().get_queryset(request).select_related()
    
    def mark_low_stock_items(self, request, queryset):
        """Custom action to identify low stock items"""
        low_stock_count = 0
        for item in queryset:
            if item.is_low_stock:
                low_stock_count += 1
        self.message_user(request, f'{low_stock_count} items are low in stock.')
    mark_low_stock_items.short_description = 'Check for low stock items'
    
    def update_reorder_level(self, request, queryset):
        """Custom action to update reorder levels"""
        updated = queryset.update(reorder_level=10)
        self.message_user(request, f'{updated} items updated with default reorder level.')
    update_reorder_level.short_description = 'Set reorder level to 10'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'quantity', 'price')
        }),
        ('Category & Supplier', {
            'fields': ('category', 'supplier', 'reorder_level')
        }),
        ('Analytics', {
            'fields': ('total_value', 'stock_status'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['item', 'transaction_type', 'quantity', 'user', 'timestamp', 'reason_short']
    list_filter = ['transaction_type', 'timestamp', 'item__category']
    search_fields = ['item__name', 'reason', 'user__username']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    list_per_page = 30
    date_hierarchy = 'timestamp'
    
    def reason_short(self, obj):
        """Display shortened reason"""
        if obj.reason:
            return obj.reason[:50] + '...' if len(obj.reason) > 50 else obj.reason
        return '-'
    reason_short.short_description = 'Reason'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        return super().get_queryset(request).select_related('item', 'user')


@admin.register(InventoryAlert)
class InventoryAlertAdmin(admin.ModelAdmin):
    list_display = ['item', 'alert_type', 'is_resolved_display', 'created_at', 'resolved_at']
    list_filter = ['alert_type', 'is_resolved', 'created_at', 'item__category']
    search_fields = ['item__name', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'resolved_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    actions = ['mark_resolved', 'mark_unresolved']
    
    def is_resolved_display(self, obj):
        """Display resolved status with better formatting"""
        return "✅ Resolved" if obj.is_resolved else "❌ Active"
    is_resolved_display.short_description = 'Status'
    is_resolved_display.admin_order_field = 'is_resolved'
    
    def mark_resolved(self, request, queryset):
        """Mark selected alerts as resolved"""
        count = 0
        for alert in queryset:
            if not alert.is_resolved:
                alert.resolve()
                count += 1
        self.message_user(request, f'{count} alerts marked as resolved.')
    mark_resolved.short_description = 'Mark selected alerts as resolved'
    
    def mark_unresolved(self, request, queryset):
        """Mark selected alerts as unresolved"""
        updated = queryset.update(is_resolved=False, resolved_at=None)
        self.message_user(request, f'{updated} alerts marked as unresolved.')
    mark_unresolved.short_description = 'Mark selected alerts as unresolved'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        return super().get_queryset(request).select_related('item')
