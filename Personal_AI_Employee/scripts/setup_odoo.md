# Odoo 17 Community Edition - Local Setup Guide

## Prerequisites

✓ Docker installed (version 29.1.3 detected)
✓ Docker Compose configuration created

## Step 1: Start Docker Desktop

**IMPORTANT**: Docker Desktop must be running before starting Odoo.

1. Open Docker Desktop application
2. Wait for the whale icon in system tray to be steady (not animated)
3. Verify Docker is running:
   ```bash
   docker --version
   docker ps
   ```

## Step 2: Start Odoo

```bash
# Navigate to project directory
cd E:\hackathon-0\Personal_AI_Employee

# Start Odoo and PostgreSQL containers
docker-compose up -d

# Check containers are running
docker-compose ps

# View logs (optional)
docker-compose logs -f odoo
```

**Expected output**:
```
Creating odoo_db  ... done
Creating odoo_app ... done
```

## Step 3: Access Odoo

Open your browser and go to:

**URL**: http://localhost:8069

You should see the Odoo database creation screen.

## Step 4: Create Database

On the first access, you'll see the database manager:

1. **Master Password**: Set a master password (save this!)
   - Example: `admin123` (change in production!)

2. **Database Name**: `odoo_production`
   - Or any name you prefer

3. **Email**: Your admin email
   - Example: `admin@company.com`

4. **Password**: Admin user password
   - Example: `admin` (change in production!)

5. **Phone Number**: Optional

6. **Language**: English (or your preference)

7. **Country**: Your country

8. **Demo Data**:
   - ✓ Check if you want sample data for testing
   - ✗ Uncheck for production

9. Click **Create Database**

**Wait 2-5 minutes** for database initialization.

## Step 5: Initial Login

After database creation:

1. You'll be automatically logged in
2. Username: `admin@company.com` (the email you entered)
3. Password: The password you set

## Step 6: Enable Required Modules

### Method 1: Via UI

1. Click **Apps** in the top menu
2. Remove the "Apps" filter to see all modules
3. Search and install:
   - **Invoicing** (Accounting Lite)
   - **Accounting** (Full Accounting)
   - **Contacts** (CRM)
   - **Sales** (Optional)

### Method 2: Via Settings

1. Go to **Settings** (gear icon)
2. Scroll to **Integrations** section
3. Enable modules as needed

## Step 7: Create API User

### Create User

1. Go to **Settings** → **Users & Companies** → **Users**
2. Click **Create**
3. Fill in details:
   - **Name**: `API User`
   - **Email**: `api@company.com`
   - **Password**: Set a strong password (save this!)

### Set Access Rights

1. In the user form, go to **Access Rights** tab
2. Grant permissions:
   - **Accounting**: Accountant or Billing
   - **Contacts**: User - All Documents
   - **Sales**: User - Own Documents Only
   - **Administration**: Settings (if needed)

3. **Save** the user

### Get API Credentials

You'll need these for API access:
- **URL**: `http://localhost:8069`
- **Database**: `odoo_production` (or your database name)
- **Username**: `api@company.com`
- **Password**: The password you set

## Step 8: Test API Connection

### Test 1: Authenticate

```bash
curl -X POST http://localhost:8069/web/session/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "db": "odoo_production",
      "login": "api@company.com",
      "password": "your_api_password"
    }
  }'
```

**Expected response**: Session ID and user info

### Test 2: Search Partners (Contacts)

```bash
curl -X POST http://localhost:8069/web/dataset/call_kw \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "model": "res.partner",
      "method": "search_read",
      "args": [[]],
      "kwargs": {
        "fields": ["name", "email", "phone"],
        "limit": 5
      }
    },
    "id": 1
  }'
```

### Test 3: Create Invoice (Python Example)

```python
import xmlrpc.client

# Connection details
url = "http://localhost:8069"
db = "odoo_production"
username = "api@company.com"
password = "your_api_password"

# Authenticate
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

# Connect to object endpoint
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Create invoice
invoice_id = models.execute_kw(
    db, uid, password,
    'account.move', 'create',
    [{
        'move_type': 'out_invoice',
        'partner_id': 1,  # Customer ID
        'invoice_date': '2026-02-16',
        'invoice_line_ids': [(0, 0, {
            'name': 'Product/Service',
            'quantity': 1,
            'price_unit': 100.00,
        })]
    }]
)

print(f"Invoice created with ID: {invoice_id}")
```

## Common Operations

### Start Odoo

```bash
docker-compose up -d
```

### Stop Odoo

```bash
docker-compose down
```

### Restart Odoo

```bash
docker-compose restart odoo
```

### View Logs

```bash
# All logs
docker-compose logs -f

# Odoo logs only
docker-compose logs -f odoo

# Database logs only
docker-compose logs -f db
```

### Access Database Directly

```bash
# Connect to PostgreSQL
docker exec -it odoo_db psql -U odoo -d odoo_production

# List databases
\l

# Connect to database
\c odoo_production

# List tables
\dt

# Exit
\q
```

### Backup Database

```bash
# Backup via Odoo UI
# Settings → Database Manager → Backup

# Or via command line
docker exec -t odoo_db pg_dump -U odoo odoo_production > odoo_backup_$(date +%Y%m%d).sql
```

### Restore Database

```bash
# Via Odoo UI
# Settings → Database Manager → Restore

# Or via command line
docker exec -i odoo_db psql -U odoo -d odoo_production < odoo_backup_20260216.sql
```

## Troubleshooting

### Issue: Cannot access http://localhost:8069

**Check containers are running**:
```bash
docker-compose ps
```

**Check Odoo logs**:
```bash
docker-compose logs odoo
```

**Restart containers**:
```bash
docker-compose restart
```

### Issue: Database connection error

**Check PostgreSQL is running**:
```bash
docker-compose ps db
```

**Check database logs**:
```bash
docker-compose logs db
```

**Verify credentials in docker-compose.yml**:
- USER=odoo
- PASSWORD=odoo
- POSTGRES_DB=postgres

### Issue: Port 8069 already in use

**Find process using port**:
```bash
# Windows
netstat -ano | findstr :8069

# Kill process (replace PID)
taskkill /PID <PID> /F
```

**Or change port in docker-compose.yml**:
```yaml
ports:
  - "8070:8069"  # Use port 8070 instead
```

### Issue: Slow performance

**Increase Docker resources**:
1. Open Docker Desktop
2. Settings → Resources
3. Increase CPU and Memory
4. Apply & Restart

### Issue: Module installation fails

**Update module list**:
1. Go to Apps
2. Click "Update Apps List"
3. Try installing again

**Check logs for errors**:
```bash
docker-compose logs -f odoo
```

## API Integration Examples

### Python (xmlrpc)

```python
import xmlrpc.client

url = "http://localhost:8069"
db = "odoo_production"
username = "api@company.com"
password = "your_password"

# Authenticate
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

# Access models
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Search partners
partners = models.execute_kw(
    db, uid, password,
    'res.partner', 'search_read',
    [[]],
    {'fields': ['name', 'email'], 'limit': 5}
)

print(partners)
```

### Node.js (odoo-xmlrpc)

```javascript
const Odoo = require('odoo-xmlrpc');

const odoo = new Odoo({
  url: 'http://localhost:8069',
  db: 'odoo_production',
  username: 'api@company.com',
  password: 'your_password'
});

odoo.connect((err) => {
  if (err) return console.error(err);

  // Search partners
  odoo.execute_kw('res.partner', 'search_read', [[]], (err, partners) => {
    if (err) return console.error(err);
    console.log(partners);
  });
});
```

### cURL (REST-like)

```bash
# Authenticate and get session
SESSION=$(curl -s -X POST http://localhost:8069/web/session/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "db": "odoo_production",
      "login": "api@company.com",
      "password": "your_password"
    }
  }' | jq -r '.result.session_id')

# Use session for requests
curl -X POST http://localhost:8069/web/dataset/call_kw \
  -H "Content-Type: application/json" \
  -H "Cookie: session_id=$SESSION" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "model": "res.partner",
      "method": "search_read",
      "args": [[]],
      "kwargs": {"fields": ["name"], "limit": 5}
    }
  }'
```

## Useful Odoo Models

| Model | Description |
|-------|-------------|
| `res.partner` | Contacts/Customers |
| `account.move` | Invoices/Bills |
| `account.payment` | Payments |
| `product.product` | Products |
| `sale.order` | Sales Orders |
| `purchase.order` | Purchase Orders |
| `stock.picking` | Deliveries |
| `project.project` | Projects |
| `project.task` | Tasks |

## Configuration Files

### docker-compose.yml

Located at: `E:\hackathon-0\Personal_AI_Employee\docker-compose.yml`

**Services**:
- `db`: PostgreSQL 15
- `odoo`: Odoo 17 Community Edition

**Ports**:
- Odoo: 8069

**Volumes**:
- `odoo-web-data`: Odoo data
- `odoo-db-data`: PostgreSQL data
- `./config`: Odoo configuration files
- `./addons`: Custom addons

### Custom Configuration (Optional)

Create `config/odoo.conf`:

```ini
[options]
admin_passwd = admin123
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
data_dir = /var/lib/odoo
logfile = /var/log/odoo/odoo.log
log_level = info
```

## Security Recommendations

### For Production

1. **Change default passwords**:
   - Master password
   - Admin user password
   - Database password
   - API user password

2. **Use environment variables**:
   ```yaml
   environment:
     - POSTGRES_PASSWORD=${DB_PASSWORD}
   ```

3. **Enable HTTPS**:
   - Use reverse proxy (nginx)
   - Get SSL certificate (Let's Encrypt)

4. **Restrict access**:
   - Firewall rules
   - VPN for admin access
   - IP whitelisting

5. **Regular backups**:
   - Automated daily backups
   - Off-site backup storage
   - Test restore procedures

## Next Steps

1. ✓ Start Docker Desktop
2. ✓ Run `docker-compose up -d`
3. ✓ Access http://localhost:8069
4. ✓ Create database
5. ✓ Enable modules (Invoicing, Accounting, Contacts)
6. ✓ Create API user
7. ✓ Test API connection
8. ✓ Integrate with AI Employee system

## Integration with AI Employee

### Invoice Generation

```python
# In orchestrator.py or invoice skill
import xmlrpc.client

def create_odoo_invoice(customer_name, amount, description):
    # Connect to Odoo
    url = "http://localhost:8069"
    db = "odoo_production"
    username = "api@company.com"
    password = os.getenv('ODOO_API_PASSWORD')

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    # Find or create customer
    partner_id = models.execute_kw(
        db, uid, password,
        'res.partner', 'search',
        [[['name', '=', customer_name]]]
    )

    if not partner_id:
        partner_id = models.execute_kw(
            db, uid, password,
            'res.partner', 'create',
            [{'name': customer_name}]
        )
    else:
        partner_id = partner_id[0]

    # Create invoice
    invoice_id = models.execute_kw(
        db, uid, password,
        'account.move', 'create',
        [{
            'move_type': 'out_invoice',
            'partner_id': partner_id,
            'invoice_date': datetime.now().strftime('%Y-%m-%d'),
            'invoice_line_ids': [(0, 0, {
                'name': description,
                'quantity': 1,
                'price_unit': amount,
            })]
        }]
    )

    return invoice_id
```

## Resources

- **Odoo Documentation**: https://www.odoo.com/documentation/17.0/
- **API Documentation**: https://www.odoo.com/documentation/17.0/developer/reference/external_api.html
- **Community Forum**: https://www.odoo.com/forum
- **Docker Hub**: https://hub.docker.com/_/odoo

---

**Status**: Ready to start

**Version**: Odoo 17 Community Edition

**Database**: PostgreSQL 15

**Access**: http://localhost:8069

**Last Updated**: 2026-02-16
