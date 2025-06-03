from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Core inventory management
    path('', views.home, name='home'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/new/', views.item_create, name='item_create'),
    path('item/<int:pk>/edit/', views.item_update, name='item_update'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('item/<int:pk>/update-stock/', views.update_stock, name='update_stock'),
    
    # User management
    path('register/', views.register, name='register'),
      # Analytics and Reporting
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('reports/', views.inventory_reports, name='reports'),
    path('reports/<str:report_type>/', views.inventory_reports, name='reports_filtered'),
    path('alerts/', views.manage_alerts, name='manage_alerts'),
    path('alerts/<int:alert_id>/resolve/', views.resolve_alert, name='resolve_alert'),
    
    # API endpoints for AJAX calls
    path('api/stock-update/<int:item_id>/', views.api_stock_update, name='api_stock_update'),
    path('api/alerts/generate/', views.api_generate_alerts, name='api_generate_alerts'),
    path('api/dashboard-data/', views.api_dashboard_data, name='api_dashboard_data'),
]
