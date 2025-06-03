#!/usr/bin/env python
"""
AWS Elastic Beanstalk deployment script for Django Inventory Management App.

This script helps automate the deployment process to AWS Elastic Beanstalk.
"""

import os
import sys
import subprocess
import argparse

def run_command(command, description=""):
    """Run a shell command and handle errors."""
    print(f"Running: {command}")
    if description:
        print(f"Description: {description}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"Success: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def deploy_to_aws(environment_name="inventory-app-env", application_name="inventory-management"):
    """Deploy the application to AWS Elastic Beanstalk."""
    
    print("Starting AWS Elastic Beanstalk deployment...")
    
    # Check if EB CLI is installed
    if not run_command("eb --version", "Checking EB CLI installation"):
        print("Please install AWS EB CLI first: pip install awsebcli")
        return False
    
    # Initialize EB if not already done
    if not os.path.exists(".elasticbeanstalk"):
        print("Initializing Elastic Beanstalk...")
        if not run_command(f"eb init {application_name} --platform python-3.9 --region us-east-1"):
            return False
    
    # Create environment if it doesn't exist
    print(f"Creating/updating environment: {environment_name}")
    if not run_command(f"eb create {environment_name} --instance-type t3.small"):
        # If create fails, try to deploy to existing environment
        if not run_command(f"eb deploy {environment_name}"):
            return False
    
    # Set environment variables
    print("Setting environment variables...")
    env_vars = [
        "DJANGO_SETTINGS_MODULE=InventoryApp.settings.production",
        "DJANGO_ENVIRONMENT=production",
    ]
    
    for var in env_vars:
        run_command(f"eb setenv {var}")
    
    print("Deployment completed!")
    print(f"Your application should be available at the EB environment URL.")
    
    # Show environment status
    run_command("eb status")
    
    return True

def setup_rds_database():
    """Set up RDS PostgreSQL database."""
    print("Setting up RDS PostgreSQL database...")
    print("Please manually create RDS instance with the following settings:")
    print("- Engine: PostgreSQL")
    print("- Instance class: db.t3.micro (for development)")
    print("- Database name: inventory_db")
    print("- Username: postgres")
    print("- Make sure to note the endpoint and password")
    print("- Configure security groups to allow access from EB environment")

def setup_s3_bucket():
    """Set up S3 bucket for static files."""
    print("Setting up S3 bucket for static files...")
    print("Please manually create S3 bucket with the following settings:")
    print("- Bucket name: your-inventory-app-static (must be globally unique)")
    print("- Region: us-east-1 (or your preferred region)")
    print("- Public access: Allow public access for static files")
    print("- CORS configuration enabled")

def main():
    parser = argparse.ArgumentParser(description="Deploy Django Inventory App to AWS")
    parser.add_argument("--deploy", action="store_true", help="Deploy to AWS EB")
    parser.add_argument("--setup-rds", action="store_true", help="Show RDS setup instructions")
    parser.add_argument("--setup-s3", action="store_true", help="Show S3 setup instructions")
    parser.add_argument("--env-name", default="inventory-app-env", help="EB environment name")
    parser.add_argument("--app-name", default="inventory-management", help="EB application name")
    
    args = parser.parse_args()
    
    if args.setup_rds:
        setup_rds_database()
    elif args.setup_s3:
        setup_s3_bucket()
    elif args.deploy:
        deploy_to_aws(args.env_name, args.app_name)
    else:
        print("Please specify an action: --deploy, --setup-rds, or --setup-s3")
        parser.print_help()

if __name__ == "__main__":
    main()
