# AWS Deployment Guide for Django Inventory Management App

## Prerequisites

1. **AWS Account**: Ensure you have an active AWS account
2. **AWS CLI**: Install and configure AWS CLI with your credentials
3. **EB CLI**: Install Elastic Beanstalk CLI (`pip install awsebcli`)
4. **PostgreSQL**: Set up RDS PostgreSQL instance
5. **S3 Bucket**: Create S3 bucket for static files

## Step-by-Step Deployment

### 1. Prepare Environment Variables

Copy `.env.example` to `.env.production` and fill in your production values:

```bash
cp .env.example .env.production
```

Required environment variables:
- `SECRET_KEY`: Generate a new secret key for production
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`: RDS PostgreSQL details
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: AWS credentials
- `AWS_STORAGE_BUCKET_NAME`: S3 bucket name
- `ALLOWED_HOSTS`: Your domain and EB environment URL

### 2. Set Up RDS PostgreSQL Database

1. Go to AWS RDS Console
2. Create new PostgreSQL database:
   - Engine: PostgreSQL
   - Instance class: db.t3.micro (for development)
   - Database name: `inventory_db`
   - Username: `postgres`
   - Set a strong password
   - Make publicly accessible: Yes (for development)
3. Configure security groups to allow access from EB environment
4. Note the endpoint URL for your environment variables

### 3. Set Up S3 Bucket for Static Files

1. Go to AWS S3 Console
2. Create new bucket:
   - Name: `your-inventory-app-static` (must be globally unique)
   - Region: `us-east-1` (or your preferred region)
   - Uncheck "Block all public access"
3. Configure CORS policy:
   ```json
   [
     {
       "AllowedHeaders": ["*"],
       "AllowedMethods": ["GET", "POST", "PUT", "DELETE"],
       "AllowedOrigins": ["*"],
       "ExposeHeaders": []
     }
   ]
   ```

### 4. Deploy to Elastic Beanstalk

1. **Initialize EB application**:
   ```bash
   eb init inventory-management --platform python-3.9 --region us-east-1
   ```

2. **Create environment**:
   ```bash
   eb create inventory-app-env --instance-type t3.small
   ```

3. **Set environment variables**:
   ```bash
   eb setenv DJANGO_SETTINGS_MODULE=InventoryApp.settings.production
   eb setenv DJANGO_ENVIRONMENT=production
   eb setenv SECRET_KEY=your-production-secret-key
   eb setenv DB_NAME=inventory_db
   eb setenv DB_USER=postgres
   eb setenv DB_PASSWORD=your-db-password
   eb setenv DB_HOST=your-rds-endpoint.amazonaws.com
   eb setenv AWS_ACCESS_KEY_ID=your-access-key
   eb setenv AWS_SECRET_ACCESS_KEY=your-secret-key
   eb setenv AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
   eb setenv ALLOWED_HOSTS=your-eb-url.elasticbeanstalk.com,yourdomain.com
   ```

4. **Deploy application**:
   ```bash
   eb deploy
   ```

### 5. Post-Deployment Steps

1. **Check application status**:
   ```bash
   eb status
   eb health
   ```

2. **View logs if needed**:
   ```bash
   eb logs
   ```

3. **Access your application**:
   - Get URL: `eb status`
   - Open in browser: `eb open`

## Automated Deployment Script

Use the provided deployment script:

```bash
# Show RDS setup instructions
python deploy_aws.py --setup-rds

# Show S3 setup instructions
python deploy_aws.py --setup-s3

# Deploy to AWS (after setting up RDS and S3)
python deploy_aws.py --deploy
```

## Security Considerations

1. **Secret Key**: Use a strong, unique secret key for production
2. **Database Security**: Restrict RDS access to EB security groups only
3. **HTTPS**: Configure SSL certificate for your domain
4. **Environment Variables**: Never commit production credentials to version control
5. **IAM Roles**: Use IAM roles instead of access keys when possible

## Monitoring and Logging

1. **CloudWatch**: Monitor application metrics and logs
2. **EB Health**: Use EB health dashboard for application monitoring
3. **Django Logging**: Check `/opt/python/log/django.log` for application logs

## Scaling

1. **Auto Scaling**: Configure auto-scaling based on CPU/memory usage
2. **Load Balancer**: EB automatically provides load balancing
3. **Database**: Consider RDS read replicas for high traffic

## Troubleshooting

1. **Deployment Issues**: Check EB logs with `eb logs`
2. **Database Connection**: Verify RDS security groups and connection details
3. **Static Files**: Ensure S3 bucket permissions are correct
4. **Environment Variables**: Double-check all required variables are set

## Cost Optimization

1. **Instance Types**: Use t3.micro for development, scale up for production
2. **RDS**: Use db.t3.micro for development
3. **S3**: Enable S3 lifecycle policies to manage costs
4. **Monitoring**: Set up billing alerts to monitor costs

## Backup and Recovery

1. **RDS Backups**: Enable automated backups for RDS
2. **Application Code**: Ensure code is in version control
3. **Environment Configuration**: Document all environment variables and configurations
