# Copilot Instructions for Inventory Management Web App

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a Django web application for inventory management built for retail businesses.

## Project Structure
- **Framework**: Django 5.2.1
- **Database**: SQLite (for development)
- **Architecture**: Django MTV (Model-Template-View) pattern
- **URL Pattern**: RESTful URLs

## Key Components
- **Models**: `Item` model with fields: name, quantity, price, created_at, updated_at
- **Views**: Function-based views for inventory operations
- **Templates**: HTML templates with Bootstrap styling
- **Admin**: Django admin interface for CRUD operations

## Development Guidelines
- Follow Django best practices and conventions
- Use function-based views for simplicity
- Implement proper error handling and validation
- Follow RESTful URL patterns
- Use Django's built-in authentication system
- Maintain clean separation between models, views, and templates

## Coding Standards
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Follow PEP 8 Python style guide
- Use Django's ORM for database operations
- Implement proper form validation
