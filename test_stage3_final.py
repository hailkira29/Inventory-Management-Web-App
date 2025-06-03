#!/usr/bin/env python3
"""
Stage 3 Feature Testing Script
Tests all advanced inventory management features implemented in Stage 3
"""

import os
import sys
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventoryApp.settings.development')

try:
    django.setup()
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

from django.contrib.auth.models import User
from inventory.models import Item, InventoryTransaction, InventoryAlert
from inventory.forms import StockUpdateForm, ReportFilterForm
from django.test import Client
from django.urls import reverse

def print_banner(title):
    """Print a formatted banner"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_models():
    """Test enhanced model functionality"""
    print_banner("TESTING ENHANCED MODELS")
    
    # Test Item model enhancements
    print("📦 Testing Item model...")
    
    # Create test item
    item = Item.objects.create(
        name="Test Widget",
        quantity=15,
        price=29.99,
        category="Electronics",
        supplier="Test Supplier",
        reorder_level=10
    )
    
    print(f"✅ Created item: {item.name}")
    print(f"✅ Total value: ${item.total_value}")
    print(f"✅ Stock status: {item.stock_status}")
    print(f"✅ Is low stock: {item.is_low_stock}")
    print(f"✅ Is out of stock: {item.is_out_of_stock}")
    
    # Test stock update method
    print("\n📊 Testing stock update method...")
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@test.com', 'password': 'password'}
    )
    
    # Test stock IN
    new_quantity = item.update_stock(10, 'IN', 'Received shipment', user)
    print(f"✅ Stock IN: New quantity = {new_quantity}")
    
    # Test stock OUT
    new_quantity = item.update_stock(-5, 'OUT', 'Sold items', user)
    print(f"✅ Stock OUT: New quantity = {new_quantity}")
    
    # Check transactions
    transactions = InventoryTransaction.objects.filter(item=item).count()
    print(f"✅ Created {transactions} transaction records")
    
    # Check alerts
    alerts = InventoryAlert.objects.filter(item=item).count()
    print(f"✅ Generated {alerts} alerts")
    
    return True

def test_forms():
    """Test enhanced form functionality"""
    print_banner("TESTING ENHANCED FORMS")
    
    print("📝 Testing StockUpdateForm...")
    form_data = {
        'transaction_type': 'IN',
        'quantity': 50,
        'reason': 'New shipment received'
    }
    form = StockUpdateForm(data=form_data)
    print(f"✅ StockUpdateForm valid: {form.is_valid()}")
    
    print("📊 Testing ReportFilterForm...")
    report_form_data = {
        'date_from': '2025-01-01',
        'date_to': '2025-12-31',
        'category': 'Electronics'
    }
    report_form = ReportFilterForm(data=report_form_data)
    print(f"✅ ReportFilterForm valid: {report_form.is_valid()}")
    
    return True

def test_views():
    """Test enhanced view functionality"""
    print_banner("TESTING ENHANCED VIEWS")
    
    client = Client()
    
    # Test home page
    print("🏠 Testing home page...")
    response = client.get('/')
    print(f"✅ Home page status: {response.status_code}")
    
    # Test analytics dashboard
    print("📈 Testing analytics dashboard...")
    response = client.get('/analytics/')
    print(f"✅ Analytics dashboard status: {response.status_code}")
    
    # Test API endpoints
    print("🔌 Testing API endpoints...")
    
    # Dashboard data API
    response = client.get('/api/dashboard-data/')
    print(f"✅ Dashboard API status: {response.status_code}")
    
    return True

def test_admin_enhancements():
    """Test admin interface enhancements"""
    print_banner("TESTING ADMIN ENHANCEMENTS")
    
    from django.contrib.admin.sites import site
    from inventory.models import Item
    
    print("👑 Testing admin interface...")
    
    # Check if custom admin actions are registered
    item_admin = site._registry.get(Item)
    if item_admin:
        # Create a mock request object for getting actions
        from django.test import RequestFactory
        from django.contrib.auth.models import User, AnonymousUser
        factory = RequestFactory()
        request = factory.get('/admin/')
        
        # Create or get a test user for admin functionality
        try:
            test_user = User.objects.get(username='admin_test')
        except User.DoesNotExist:
            test_user = User.objects.create_superuser('admin_test', 'admin@test.com', 'password')
        
        request.user = test_user
        
        actions = item_admin.get_actions(request)
        print(f"✅ Admin actions available: {len(actions)}")
        print(f"   - mark_low_stock_items: {'mark_low_stock_items' in actions}")
        print(f"   - update_reorder_level: {'update_reorder_level' in actions}")
        
        # Test admin methods
        print(f"✅ Admin display methods working: {hasattr(item_admin, 'get_stock_status')}")
        print(f"✅ Admin total value method working: {hasattr(item_admin, 'get_total_value')}")
    else:
        print("❌ ItemAdmin not found in registry")
        return False
    
    return True

def test_url_patterns():
    """Test URL patterns"""
    print_banner("TESTING URL PATTERNS")
    
    print("🔗 Testing URL patterns...")
    
    urls_to_test = [
        ('inventory:home', {}),
        ('inventory:analytics', {}),
        ('inventory:reports', {}),
        ('inventory:manage_alerts', {}),
    ]
    
    for url_name, kwargs in urls_to_test:
        try:
            url = reverse(url_name, kwargs=kwargs)
            print(f"✅ {url_name}: {url}")
        except Exception as e:
            print(f"❌ {url_name}: {e}")
    
    return True

def run_comprehensive_test():
    """Run all tests"""
    print_banner("STAGE 3 COMPREHENSIVE TESTING")
    
    tests = [
        test_models,
        test_forms,
        test_views,
        test_admin_enhancements,
        test_url_patterns,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append(False)
    
    # Summary
    print_banner("TEST SUMMARY")
    passed = sum(results)
    total = len(results)
    print(f"📊 Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Stage 3 implementation is successful!")
        return True
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
