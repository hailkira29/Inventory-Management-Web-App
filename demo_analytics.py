#!/usr/bin/env python3
"""
Stage 3 Analytics Features Demonstration
Django Inventory Management App
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventoryApp.settings')
django.setup()

from inventory.models import Item, InventoryTransaction, InventoryAlert
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum, Count, Avg, F

def create_demo_data():
    """Create sample data to demonstrate analytics features"""
    print("🚀 Creating sample data for analytics demonstration...")
    
    # Categories and suppliers
    categories = ['Electronics', 'Clothing', 'Books', 'Tools', 'Food', 'Sports']
    suppliers = ['TechCorp', 'FashionHub', 'BookWorld', 'ToolMaster', 'FreshFoods', 'SportsPro']
    
    # Create sample items if they don't exist
    sample_items = [
        {'name': 'Laptop Computer', 'category': 'Electronics', 'supplier': 'TechCorp', 'price': 999.99, 'quantity': 15, 'reorder_level': 5},
        {'name': 'Wireless Mouse', 'category': 'Electronics', 'supplier': 'TechCorp', 'price': 29.99, 'quantity': 50, 'reorder_level': 10},
        {'name': 'Cotton T-Shirt', 'category': 'Clothing', 'supplier': 'FashionHub', 'price': 19.99, 'quantity': 3, 'reorder_level': 10},  # Low stock
        {'name': 'Python Programming Book', 'category': 'Books', 'supplier': 'BookWorld', 'price': 49.99, 'quantity': 25, 'reorder_level': 5},
        {'name': 'Screwdriver Set', 'category': 'Tools', 'supplier': 'ToolMaster', 'price': 39.99, 'quantity': 0, 'reorder_level': 5},  # Out of stock
        {'name': 'Organic Apples', 'category': 'Food', 'supplier': 'FreshFoods', 'price': 4.99, 'quantity': 100, 'reorder_level': 20},
        {'name': 'Basketball', 'category': 'Sports', 'supplier': 'SportsPro', 'price': 24.99, 'quantity': 8, 'reorder_level': 3},
        {'name': 'Smartphone', 'category': 'Electronics', 'supplier': 'TechCorp', 'price': 699.99, 'quantity': 2, 'reorder_level': 5},  # Low stock
    ]
    
    items_created = 0
    for item_data in sample_items:
        item, created = Item.objects.get_or_create(
            name=item_data['name'],
            defaults=item_data
        )
        if created:
            items_created += 1
            print(f"  ✅ Created item: {item.name}")
    
    print(f"📦 Created {items_created} new items")
    
    # Create sample transactions
    items = Item.objects.all()
    user = User.objects.first()
    if not user:
        user = User.objects.create_user('demo_user', 'demo@example.com', 'password123')
        print("👤 Created demo user")
    
    transaction_types = ['STOCK_IN', 'STOCK_OUT', 'ADJUSTMENT']
    transactions_created = 0
    
    for _ in range(20):  # Create 20 sample transactions
        item = random.choice(items)
        transaction_type = random.choice(transaction_types)
        
        if transaction_type == 'STOCK_IN':
            quantity = random.randint(5, 50)
        elif transaction_type == 'STOCK_OUT':
            quantity = -random.randint(1, min(10, item.quantity))
        else:  # ADJUSTMENT
            quantity = random.randint(-5, 5)
        
        # Create transaction from 1-30 days ago
        created_at = timezone.now() - timedelta(days=random.randint(1, 30))
        
        transaction = InventoryTransaction.objects.create(
            item=item,
            transaction_type=transaction_type,
            quantity=quantity,
            notes=f"Demo {transaction_type.lower()} transaction",
            created_by=user,
            created_at=created_at
        )
        transactions_created += 1
    
    print(f"📊 Created {transactions_created} sample transactions")
    
    # Generate alerts for low stock and out of stock items
    alerts_created = 0
    low_stock_items = Item.objects.filter(quantity__lte=F('reorder_level'), quantity__gt=0)
    for item in low_stock_items:
        alert, created = InventoryAlert.objects.get_or_create(
            item=item,
            alert_type='LOW_STOCK',
            is_resolved=False,
            defaults={
                'message': f'Item "{item.name}" is running low. Current stock: {item.quantity}, Reorder level: {item.reorder_level}',
                'created_at': timezone.now()
            }
        )
        if created:
            alerts_created += 1
    
    out_of_stock_items = Item.objects.filter(quantity=0)
    for item in out_of_stock_items:
        alert, created = InventoryAlert.objects.get_or_create(
            item=item,
            alert_type='OUT_OF_STOCK',
            is_resolved=False,
            defaults={
                'message': f'Item "{item.name}" is out of stock. Immediate restocking required.',
                'created_at': timezone.now()
            }
        )
        if created:
            alerts_created += 1
    
    print(f"🚨 Created {alerts_created} alerts")
    
    return items_created, transactions_created, alerts_created

def demonstrate_analytics():
    """Demonstrate analytics features"""
    print("\n📈 ANALYTICS DEMONSTRATION")
    print("=" * 50)
    
    # Basic metrics
    total_items = Item.objects.count()
    total_value = Item.objects.aggregate(
        total=Sum(F('quantity') * F('price'))
    )['total'] or 0
    
    print(f"📦 Total Items: {total_items}")
    print(f"💰 Total Inventory Value: ${total_value:,.2f}")
    
    # Category breakdown
    print("\n📊 Category Breakdown:")
    categories = Item.objects.values('category').annotate(
        count=Count('id'),
        total_quantity=Sum('quantity'),
        total_value=Sum(F('quantity') * F('price'))
    ).order_by('-count')
    
    for cat in categories:
        print(f"  {cat['category']}: {cat['count']} items, "
              f"Qty: {cat['total_quantity']}, "
              f"Value: ${(cat['total_value'] or 0):,.2f}")
    
    # Stock status
    print("\n📊 Stock Status:")
    low_stock = Item.objects.filter(quantity__lte=F('reorder_level')).count()
    out_of_stock = Item.objects.filter(quantity=0).count()
    in_stock = Item.objects.filter(quantity__gt=F('reorder_level')).count()
    
    print(f"  ✅ In Stock: {in_stock} items")
    print(f"  ⚠️  Low Stock: {low_stock} items")
    print(f"  ❌ Out of Stock: {out_of_stock} items")
    
    # Recent transactions
    print("\n📋 Recent Transactions:")
    recent_transactions = InventoryTransaction.objects.select_related('item', 'created_by').order_by('-created_at')[:5]
    for trans in recent_transactions:
        print(f"  {trans.created_at.strftime('%Y-%m-%d')}: {trans.item.name} "
              f"({trans.transaction_type}) Qty: {trans.quantity}")
    
    # Active alerts
    print("\n🚨 Active Alerts:")
    active_alerts = InventoryAlert.objects.filter(is_resolved=False).select_related('item')
    if active_alerts:
        for alert in active_alerts:
            print(f"  {alert.alert_type}: {alert.item.name} - {alert.message}")
    else:
        print("  No active alerts")
    
    print("\n" + "=" * 50)
    print("✅ Analytics demonstration complete!")

def show_urls():
    """Show the analytics URLs available"""
    print("\n🌐 ANALYTICS URLS AVAILABLE:")
    print("=" * 50)
    print("📊 Analytics Dashboard: http://127.0.0.1:8000/analytics/")
    print("📈 Reports: http://127.0.0.1:8000/reports/")
    print("🚨 Manage Alerts: http://127.0.0.1:8000/alerts/")
    print("🏠 Home: http://127.0.0.1:8000/")
    print("⚙️  Admin: http://127.0.0.1:8000/admin/")

def main():
    """Main demonstration function"""
    print("🎯 DJANGO INVENTORY MANAGEMENT APP")
    print("📊 STAGE 3: ANALYTICS FEATURES DEMONSTRATION")
    print("=" * 60)
    print(f"🕒 Started at: {datetime.now()}")
    print()
    
    try:
        # Create sample data
        items, transactions, alerts = create_demo_data()
        
        # Demonstrate analytics
        demonstrate_analytics()
        
        # Show available URLs
        show_urls()
        
        print(f"\n🎉 Demonstration completed successfully!")
        print(f"📝 Sample data created: {items} items, {transactions} transactions, {alerts} alerts")
        print("\n💡 TIP: Start the Django server with 'python manage.py runserver' and visit the URLs above!")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
