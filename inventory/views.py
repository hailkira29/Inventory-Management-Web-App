from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, Avg, F
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .models import Item, InventoryTransaction, InventoryAlert
from .forms import ItemForm, CustomUserCreationForm, StockUpdateForm, ReportFilterForm
import json


def home(request):
    """Home view that displays all inventory items with search functionality"""
    search_query = request.GET.get('search', '')
    items = Item.objects.all()
    
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) |
            Q(price__icontains=search_query)
        )
    
    context = {
        'items': items,
        'search_query': search_query,
    }
    return render(request, 'inventory/item_list.html', context)


@login_required
def item_detail(request, pk):
    """Display detailed view of a specific item"""
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'inventory/item_detail.html', {'item': item})


@login_required
def item_create(request):
    """Create a new inventory item"""
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f'Item "{item.name}" created successfully!')
            return redirect('inventory:item_detail', pk=item.pk)
    else:
        form = ItemForm()
    
    return render(request, 'inventory/item_form.html', {
        'form': form,
        'title': 'Add New Item',
        'button_text': 'Create Item'
    })


@login_required
def item_update(request, pk):
    """Update an existing inventory item"""
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            messages.success(request, f'Item "{item.name}" updated successfully!')
            return redirect('inventory:item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'inventory/item_form.html', {
        'form': form,
        'item': item,
        'title': f'Edit {item.name}',
        'button_text': 'Update Item'
    })


@login_required
def item_delete(request, pk):
    """Delete an inventory item"""
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == 'POST':
        item_name = item.name
        item.delete()
        messages.success(request, f'Item "{item_name}" deleted successfully!')
        return redirect('inventory:home')
    
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('inventory:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Inventory Management.')
            return redirect('inventory:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def analytics_dashboard(request):
    """Analytics dashboard with inventory insights"""
    # Basic statistics
    total_items = Item.objects.count()
    total_value = Item.objects.aggregate(
        total=Sum('quantity') * Sum('price')
    )['total'] or 0
    
    low_stock_items = Item.objects.filter(quantity__lte=F('reorder_level')).count()
    out_of_stock_items = Item.objects.filter(quantity=0).count()
    
    # Category breakdown
    category_data = Item.objects.values('category').annotate(
        count=Count('id'),
        total_value=Sum(F('quantity') * F('price'))
    ).order_by('-total_value')
    
    # Stock status distribution
    stock_status_data = {
        'in_stock': Item.objects.filter(quantity__gt=F('reorder_level')).count(),
        'low_stock': low_stock_items,
        'out_of_stock': out_of_stock_items,
    }
    
    # Recent transactions
    recent_transactions = InventoryTransaction.objects.select_related('item', 'user')[:10]
    
    # Active alerts
    active_alerts = InventoryAlert.objects.filter(is_resolved=False).select_related('item')[:5]
    
    # Monthly trends (last 6 months)
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_data = []
    for i in range(6):
        month_start = six_months_ago + timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        month_transactions = InventoryTransaction.objects.filter(
            timestamp__range=[month_start, month_end]
        ).count()
        monthly_data.append({
            'month': month_start.strftime('%b %Y'),
            'transactions': month_transactions
        })
    
    context = {
        'total_items': total_items,
        'total_value': total_value,
        'low_stock_items': low_stock_items,
        'out_of_stock_items': out_of_stock_items,
        'category_data': category_data,
        'stock_status_data': stock_status_data,
        'recent_transactions': recent_transactions,
        'active_alerts': active_alerts,
        'monthly_data': json.dumps(monthly_data),
    }
    
    return render(request, 'inventory/analytics_dashboard.html', context)


@login_required
def inventory_reports(request):
    """Generate various inventory reports"""
    report_type = request.GET.get('type', 'stock_levels')
    
    if report_type == 'stock_levels':
        # Stock levels report
        items = Item.objects.all().order_by('quantity')
        context = {
            'report_title': 'Stock Levels Report',
            'items': items,
            'report_type': 'stock_levels',
        }
    
    elif report_type == 'low_stock':
        # Low stock report
        items = Item.objects.filter(quantity__lte=F('reorder_level'))
        context = {
            'report_title': 'Low Stock Alert Report',
            'items': items,
            'report_type': 'low_stock',
        }
    
    elif report_type == 'category_summary':
        # Category summary report
        categories = Item.objects.values('category').annotate(
            item_count=Count('id'),
            total_quantity=Sum('quantity'),
            total_value=Sum(F('quantity') * F('price')),
            avg_price=Avg('price')
        ).order_by('category')
        context = {
            'report_title': 'Category Summary Report',
            'categories': categories,
            'report_type': 'category_summary',
        }
    
    else:
        # Default to stock levels
        items = Item.objects.all()
        context = {
            'report_title': 'All Items Report',
            'items': items,
            'report_type': 'all_items',
        }
    
    return render(request, 'inventory/reports.html', context)


@login_required
def manage_alerts(request):
    """Manage inventory alerts"""
    active_alerts = InventoryAlert.objects.filter(is_resolved=False).select_related('item')
    resolved_alerts = InventoryAlert.objects.filter(is_resolved=True).select_related('item')[:20]
    
    # Generate new alerts for low stock items
    low_stock_items = Item.objects.filter(
        quantity__lte=F('reorder_level'),
        quantity__gt=0
    )
    
    for item in low_stock_items:
        # Check if alert already exists
        existing_alert = InventoryAlert.objects.filter(
            item=item,
            alert_type='LOW_STOCK',
            is_resolved=False
        ).exists()
        
        if not existing_alert:
            InventoryAlert.objects.create(
                item=item,
                alert_type='LOW_STOCK',
                message=f'Item "{item.name}" is running low. Current stock: {item.quantity}, Reorder level: {item.reorder_level}'
            )
    
    # Generate alerts for out of stock items
    out_of_stock_items = Item.objects.filter(quantity=0)
    
    for item in out_of_stock_items:
        existing_alert = InventoryAlert.objects.filter(
            item=item,
            alert_type='OUT_OF_STOCK',
            is_resolved=False
        ).exists()
        
        if not existing_alert:
            InventoryAlert.objects.create(
                item=item,
                alert_type='OUT_OF_STOCK',
                message=f'Item "{item.name}" is out of stock. Immediate restocking required.'
            )
    
    context = {
        'active_alerts': active_alerts,
        'resolved_alerts': resolved_alerts,
    }
    
    return render(request, 'inventory/manage_alerts.html', context)


@login_required
def resolve_alert(request, alert_id):
    """Resolve a specific alert"""
    alert = get_object_or_404(InventoryAlert, id=alert_id)
    alert.resolve()
    messages.success(request, f'Alert for "{alert.item.name}" has been resolved.')
    return redirect('inventory:manage_alerts')


@login_required
def update_stock(request, pk):
    """Update stock levels for an item"""
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == 'POST':
        form = StockUpdateForm(request.POST)
        if form.is_valid():
            transaction_type = form.cleaned_data['transaction_type']
            quantity = form.cleaned_data['quantity']
            reason = form.cleaned_data['reason']
            
            try:
                # Calculate quantity change based on transaction type
                if transaction_type == 'IN':
                    quantity_change = quantity
                elif transaction_type == 'OUT':
                    quantity_change = -quantity
                else:  # ADJUST
                    # For adjustment, the quantity is the new total quantity
                    quantity_change = quantity - item.quantity
                
                # Update stock using the model method
                new_quantity = item.update_stock(
                    quantity_change=quantity_change,
                    transaction_type=transaction_type,
                    reason=reason,
                    user=request.user
                )
                
                messages.success(
                    request, 
                    f'Stock updated for "{item.name}". New quantity: {new_quantity}'
                )
                return redirect('inventory:item_detail', pk=item.pk)
                
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = StockUpdateForm()
    
    context = {
        'item': item,
        'form': form,
        'title': f'Update Stock - {item.name}'
    }
    return render(request, 'inventory/stock_update.html', context)


def api_stock_update(request, item_id):
    """API endpoint for updating stock via AJAX"""
    if request.method == 'POST':
        try:
            item = get_object_or_404(Item, pk=item_id)
            data = json.loads(request.body)
            
            transaction_type = data.get('transaction_type')
            quantity = int(data.get('quantity', 0))
            reason = data.get('reason', '')
            
            if transaction_type == 'IN':
                quantity_change = quantity
            elif transaction_type == 'OUT':
                quantity_change = -quantity
            else:
                quantity_change = quantity - item.quantity
            
            new_quantity = item.update_stock(
                quantity_change=quantity_change,
                transaction_type=transaction_type,
                reason=reason,
                user=request.user if request.user.is_authenticated else None
            )
            
            return JsonResponse({
                'success': True,
                'new_quantity': new_quantity,
                'message': f'Stock updated successfully. New quantity: {new_quantity}'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def api_generate_alerts(request):
    """API endpoint to generate alerts for all items"""
    if request.method == 'POST':
        try:
            generated_count = 0
            items = Item.objects.all()
            
            for item in items:
                old_alerts_count = InventoryAlert.objects.filter(
                    item=item, is_resolved=False
                ).count()
                
                item.check_and_create_alerts()
                
                new_alerts_count = InventoryAlert.objects.filter(
                    item=item, is_resolved=False
                ).count()
                
                if new_alerts_count > old_alerts_count:
                    generated_count += (new_alerts_count - old_alerts_count)
            
            return JsonResponse({
                'success': True,
                'generated_count': generated_count,
                'message': f'{generated_count} new alerts generated.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def api_dashboard_data(request):
    """API endpoint for dashboard data (for dynamic updates)"""
    try:
        # Basic statistics
        total_items = Item.objects.count()
        total_value = Item.objects.aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or 0
        
        low_stock_items = Item.objects.filter(quantity__lte=F('reorder_level')).count()
        out_of_stock_items = Item.objects.filter(quantity=0).count()
        
        # Recent alerts
        recent_alerts = InventoryAlert.objects.filter(
            is_resolved=False
        ).select_related('item').order_by('-created_at')[:5]
        
        alerts_data = []
        for alert in recent_alerts:
            alerts_data.append({
                'id': alert.id,
                'item_name': alert.item.name,
                'alert_type': alert.get_alert_type_display(),
                'message': alert.message,
                'created_at': alert.created_at.strftime('%Y-%m-%d %H:%M')
            })
        
        data = {
            'total_items': total_items,
            'total_value': float(total_value),
            'low_stock_items': low_stock_items,
            'out_of_stock_items': out_of_stock_items,
            'recent_alerts': alerts_data,
            'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return JsonResponse({'success': True, 'data': data})
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# Add JsonResponse import workaround
try:
    from django.http import JsonResponse
except ImportError:
    # Fallback for older Django versions or missing imports
    from django.http import HttpResponse
    import json
    
    def JsonResponse(data, **kwargs):
        return HttpResponse(
            json.dumps(data),
            content_type='application/json',
            **kwargs
        )

# Custom error handlers for production
def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'inventory/errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error handler"""
    return render(request, 'inventory/errors/500.html', status=500)
