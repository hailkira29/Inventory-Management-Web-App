# 🏪 Django Inventory Management System

[![Django](https://img.shields.io/badge/Django-5.2.1-green.svg)](https://djangoproject.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-purple.svg)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive, feature-rich inventory management web application built with Django 5.2.1. Perfect for retail businesses, warehouses, and any organization that needs to track inventory with advanced analytics and reporting capabilities.

## ✨ Features

### 🎯 Core Functionality
- **Complete Item Management**: Full CRUD operations with advanced filtering
- **Real-time Stock Tracking**: Live inventory levels with automatic updates
- **Transaction History**: Detailed audit trail of all inventory movements
- **Smart Alerts**: Automated low-stock and out-of-stock notifications
- **Multi-user Support**: Role-based access with Django's authentication system

### 📊 Advanced Analytics (Stage 3)
- **Interactive Dashboard**: Beautiful charts and visualizations using Plotly
- **Comprehensive Reporting**: Advanced reports with date filtering and export
- **Stock Movement API**: RESTful endpoints for inventory operations
- **Enhanced Admin Interface**: Custom admin actions and bulk operations
- **Real-time Notifications**: Instant alerts for critical inventory events
- **Category Analysis**: Detailed insights by product categories
- **Supplier Management**: Track and analyze supplier performance

### 💻 Modern UI/UX
- **Responsive Design**: Mobile-first design that works on all devices
- **Professional Interface**: Clean, intuitive design with Bootstrap 5
- **Dashboard Overview**: Comprehensive inventory status at a glance
- **Custom Error Pages**: Friendly error handling with helpful messages
- **Accessibility**: WCAG compliant interface design

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 5.2.1, Python 3.8+ |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Charts** | Plotly.js for interactive visualizations |
| **Authentication** | Django's built-in auth system |
| **Deployment** | AWS Elastic Beanstalk ready |
| **Static Files** | WhiteNoise for production |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool (venv/virtualenv)

### 1. Clone & Setup
```bash
git clone https://github.com/hailkira29/Inventory-Management-Web-App.git
cd Inventory-Management-Web-App

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings (required):
SECRET_KEY=your-super-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 4. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Load Demo Data (Optional)
```bash
python demo_analytics.py
```

### 6. Run Development Server
```bash
python manage.py runserver
```

🎉 **Visit http://127.0.0.1:8000 to access your inventory management system!**

## 🧪 Testing

Run the comprehensive test suite to verify all features:

```bash
# Run all Stage 3 tests
python test_stage3_final.py

# Expected output: ✅ 5/5 tests passed
```

Tests cover:
- ✅ Enhanced models and properties
- ✅ Form validation and processing  
- ✅ View functionality and API endpoints
- ✅ Admin interface enhancements
- ✅ URL routing and patterns

## 📁 Project Architecture

```
django-inventory-management/
├── 📂 inventory/                    # Main application
│   ├── 🐍 models.py                # Data models (Item, Transaction, Alert)
│   ├── 🎨 views.py                 # Business logic and API endpoints
│   ├── 📝 forms.py                 # Form definitions and validation
│   ├── ⚙️  admin.py                 # Enhanced admin interface
│   ├── 🔗 urls.py                  # URL routing
│   ├── 📂 templates/               # HTML templates
│   │   ├── 📂 inventory/           # App-specific templates
│   │   └── 📂 registration/        # Auth templates
│   └── 📂 migrations/              # Database migrations
├── 📂 InventoryApp/                # Project configuration
│   ├── 📂 settings/                # Environment-specific settings
│   │   ├── 🔧 base.py              # Base configuration
│   │   ├── 🛠️  development.py       # Development settings
│   │   └── 🚀 production.py        # Production settings
│   ├── 🔗 urls.py                  # Main URL configuration
│   └── 🌐 wsgi.py                  # WSGI configuration
├── 📂 static/                      # Static files (CSS, JS, images)
├── 📋 requirements.txt             # Python dependencies
├── 🔧 manage.py                    # Django management
└── 📖 README.md                    # This file
```

## 🎯 Key Features Deep Dive

### 📊 Analytics Dashboard
- **Real-time Metrics**: Live inventory counts, values, and trends
- **Interactive Charts**: Plotly-powered visualizations with drill-down capabilities
- **Category Analysis**: Performance insights by product categories
- **Trend Analysis**: Historical data visualization with customizable time ranges

### 📦 Stock Management
- **Bulk Operations**: Update multiple items simultaneously
- **Transaction Tracking**: Complete audit trail of stock movements
- **Automated Alerts**: Smart notifications for reorder points
- **Supplier Integration**: Comprehensive supplier information management

### 📈 Advanced Reporting
- **Custom Reports**: Generate reports based on various criteria
- **Export Capabilities**: Download reports in multiple formats
- **Date Range Filtering**: Flexible time-based analysis
- **Alert Management**: Comprehensive alert history and resolution tracking

### 🔧 Enhanced Admin
- **Custom Actions**: Bulk operations for inventory management
- **Advanced Filtering**: Multi-parameter search and filtering
- **Calculated Fields**: Real-time computed values in admin lists
- **User-friendly Interface**: Improved admin experience with custom templates

## 🚀 Deployment

### AWS Elastic Beanstalk (Recommended)
```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init
eb create inventory-management-prod
eb deploy
```

See `AWS_DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

### Docker Deployment
```bash
# Build and run with Docker
docker build -t inventory-management .
docker run -p 8000:8000 inventory-management
```

### Traditional Server
- Configure with gunicorn/uWSGI
- Set up nginx for static files
- Use PostgreSQL for production database

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | **Required** |
| `DEBUG` | Debug mode | `False` |
| `DATABASE_URL` | Database connection | `sqlite:///db.sqlite3` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` |

### Production Settings
- Automatic static file collection
- Database connection pooling
- Security middleware enabled
- HTTPS redirection support

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with clear, commented code
4. **Add tests** for new functionality
5. **Ensure all tests pass**: `python test_stage3_final.py`
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Create Pull Request** with detailed description

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions and classes
- Include tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Help

- 📚 **Documentation**: Check the `/docs` folder for detailed guides
- 🐛 **Bug Reports**: Open an issue on GitHub with detailed description
- 💡 **Feature Requests**: Submit enhancement ideas via GitHub issues
- ❓ **Questions**: Use GitHub Discussions for general questions

## 🎉 Acknowledgments

- **Django Team** - For the amazing web framework
- **Bootstrap Team** - For the responsive UI framework  
- **Plotly Team** - For the interactive charting library
- **Community Contributors** - For feedback and contributions

---

**Made with ❤️ using Django** | **Star ⭐ this repo if you find it helpful!**
