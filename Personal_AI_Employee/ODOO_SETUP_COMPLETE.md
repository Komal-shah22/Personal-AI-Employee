# Odoo 17 Community Edition - Setup Complete

## ✅ Status: READY TO START

All Odoo setup files have been created. Docker Desktop needs to be started before launching Odoo.

## What Was Created

### 1. Docker Configuration ✓

**File**: `docker-compose.yml`

**Services**:
- **Odoo 17 Community Edition** (port 8069)
- **PostgreSQL 15** (database)

**Volumes**:
- `odoo-web-data` - Odoo application data
- `odoo-db-data` - PostgreSQL database
- `./config` - Odoo configuration files
- `./addons` - Custom addons directory

### 2. Quick Start Scripts ✓

**Windows**: `scripts/start_odoo.bat`
- Checks Docker Desktop is running
- Pulls Docker images
- Starts containers
- Waits for Odoo to be ready

**Mac/Linux**: `scripts/start_odoo.sh`
- Same functionality as Windows script
- Executable permissions set

### 3. Comprehensive Setup Guide ✓

**File**: `scripts/setup_odoo.md` (1000+ lines)

**Sections**:
- Prerequisites and Docker setup
- Starting Odoo containers
- Database creation walkthrough
- Module installation (Invoicing, Accounting, Contacts)
- API user creation with access rights
- API connection testing (cURL, Python, Node.js)
- Common operations (start, stop, backup, restore)
- Troubleshooting guide
- Integration examples with AI Employee
- Security recommendations

### 4. Connection Test Script ✓

**File**: `scripts/test_odoo_connection.py`

**Tests**:
1. Connection to Odoo server
2. Authentication with credentials
3. Read partners (contacts)
4. Check installed modules
5. Create test partner (optional)

**Features**:
- Detailed error messages
- Troubleshooting suggestions
- Success/failure indicators

## Quick Start Guide

### Step 1: Start Docker Desktop

**IMPORTANT**: Docker Desktop must be running first.

1. Open Docker Desktop application
2. Wait for whale icon to be steady (not animated)
3. Verify: `docker ps` should work without errors

### Step 2: Start Odoo

**Windows**:
```cmd
scripts\start_odoo.bat
```

**Mac/Linux**:
```bash
./scripts/start_odoo.sh
```

**What it does**:
- Checks Docker is running
- Pulls Odoo 17 and PostgreSQL 15 images
- Starts both containers
- Waits 30 seconds for initialization
- Shows container status

### Step 3: Access Odoo

Open browser: **http://localhost:8069**

You should see the Odoo database creation screen.

### Step 4: Create Database

On first access:

1. **Master Password**: `admin123` (change in production!)
2. **Database Name**: `odoo_production`
3. **Email**: `admin@company.com`
4. **Password**: `admin` (change in production!)
5. **Language**: English
6. **Country**: Your country
7. **Demo Data**: ✓ Check for testing, ✗ Uncheck for production

Click **Create Database** and wait 2-5 minutes.

### Step 5: Enable Modules

After login:

1. Click **Apps** in top menu
2. Remove "Apps" filter to see all modules
3. Search and install:
   - **Invoicing** (Accounting Lite)
   - **Accounting** (Full Accounting)
   - **Contacts** (CRM)

### Step 6: Create API User

1. Go to **Settings** → **Users & Companies** → **Users**
2. Click **Create**
3. Fill in:
   - Name: `API User`
   - Email: `api@company.com`
   - Password: Set strong password
4. Set **Access Rights**:
   - Accounting: Accountant
   - Contacts: User - All Documents
   - Sales: User - Own Documents Only
5. **Save**

### Step 7: Test Connection

Edit `scripts/test_odoo_connection.py`:

```python
ODOO_DB = "odoo_production"  # Your database name
ODOO_USERNAME = "api@company.com"  # Your API user
ODOO_PASSWORD = "your_password"  # Your API password
```

Run test:

```bash
python scripts/test_odoo_connection.py
```

**Expected output**:
```
============================================================
ODOO API CONNECTION TEST
============================================================

============================================================
TEST 1: CONNECTION
============================================================
✓ Connected to Odoo successfully
  Server version: 17.0
  Protocol version: 1

============================================================
TEST 2: AUTHENTICATION
============================================================
✓ Authentication successful
  User ID: 2

============================================================
TEST 3: READ PARTNERS
============================================================
✓ Found 3 partners

============================================================
TEST 4: CHECK MODULES
============================================================
✓ Module 'account' is installed
✓ Module 'contacts' is installed
✓ Module 'base' is installed

============================================================
ALL TESTS COMPLETED
============================================================

✓ Odoo API is working correctly!
```

## Common Commands

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

# Odoo only
docker-compose logs -f odoo
```

### Check Status
```bash
docker-compose ps
```

### Backup Database
```bash
# Via Odoo UI: Settings → Database Manager → Backup

# Or command line
docker exec -t odoo_db pg_dump -U odoo odoo_production > odoo_backup_$(date +%Y%m%d).sql
```

## Integration with AI Employee

### Invoice Generation Example

```python
# In orchestrator.py or invoice_skill.py
import xmlrpc.client
import os

def create_invoice_in_odoo(customer_name, amount, description):
    """Create invoice in Odoo"""

    # Connect to Odoo
    url = "http://localhost:8069"
    db = "odoo_production"
    username = "api@company.com"
    password = os.getenv('ODOO_API_PASSWORD')

    # Authenticate
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})

    if not uid:
        raise Exception("Odoo authentication failed")

    # Connect to models
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    # Find or create customer
    partner_ids = models.execute_kw(
        db, uid, password,
        'res.partner', 'search',
        [[['name', '=', customer_name]]]
    )

    if not partner_ids:
        # Create customer
        partner_id = models.execute_kw(
            db, uid, password,
            'res.partner', 'create',
            [{'name': customer_name, 'customer_rank': 1}]
        )
    else:
        partner_id = partner_ids[0]

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

### Add to Invoice Skill

Edit `.claude/skills/invoice_skill.md`:

```markdown
## Invoice Generation Process

1. Read invoice request from Needs_Action/
2. Extract: customer name, amount, description
3. Create invoice in Odoo via API
4. Generate PDF (Odoo handles this)
5. Send email with invoice attached
6. Move request to Done/
```

### Environment Variables

Add to `.env`:

```bash
# Odoo Configuration
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_production
ODOO_API_USER=api@company.com
ODOO_API_PASSWORD=your_secure_password
```

## Troubleshooting

### Issue: Cannot access http://localhost:8069

**Solution**:
```bash
# Check Docker Desktop is running
docker ps

# Check containers are running
docker-compose ps

# Check Odoo logs
docker-compose logs odoo

# Restart containers
docker-compose restart
```

### Issue: "Docker Desktop is not running"

**Solution**:
1. Open Docker Desktop application
2. Wait for it to fully start
3. Check system tray for whale icon
4. Run script again

### Issue: Port 8069 already in use

**Solution**:
```bash
# Windows - find process
netstat -ano | findstr :8069

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
ports:
  - "8070:8069"  # Use 8070 instead
```

### Issue: Database creation fails

**Solution**:
- Check PostgreSQL container is running: `docker-compose ps db`
- Check database logs: `docker-compose logs db`
- Restart containers: `docker-compose restart`

### Issue: API authentication fails

**Solution**:
- Verify database name is correct
- Verify username (email) is correct
- Verify password is correct
- Check user exists in Odoo: Settings → Users
- Check user has API access rights

## File Structure

```
Personal_AI_Employee/
├── docker-compose.yml              # Docker configuration
├── config/                         # Odoo config files (optional)
├── addons/                         # Custom addons (optional)
└── scripts/
    ├── setup_odoo.md              # Comprehensive guide (1000+ lines)
    ├── start_odoo.bat             # Windows start script
    ├── start_odoo.sh              # Mac/Linux start script
    └── test_odoo_connection.py    # Connection test script
```

## Security Recommendations

### For Production

1. **Change all default passwords**:
   - Master password
   - Admin user password
   - Database password (in docker-compose.yml)
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
   - Off-site storage
   - Test restore procedures

## Next Steps

1. ✓ Start Docker Desktop
2. ✓ Run `scripts/start_odoo.bat` (Windows) or `./scripts/start_odoo.sh` (Mac/Linux)
3. ✓ Access http://localhost:8069
4. ✓ Create database
5. ✓ Enable modules (Invoicing, Accounting, Contacts)
6. ✓ Create API user
7. ✓ Test connection with `python scripts/test_odoo_connection.py`
8. ✓ Integrate with AI Employee orchestrator
9. ✓ Create invoice generation workflow
10. ✓ Set up automated accounting tasks

## Resources

- **Setup Guide**: `scripts/setup_odoo.md`
- **Odoo Documentation**: https://www.odoo.com/documentation/17.0/
- **API Documentation**: https://www.odoo.com/documentation/17.0/developer/reference/external_api.html
- **Docker Hub**: https://hub.docker.com/_/odoo
- **Community Forum**: https://www.odoo.com/forum

## Summary

Odoo 17 Community Edition is ready to be deployed locally:

✓ Docker configuration created
✓ Quick start scripts for Windows and Mac/Linux
✓ Comprehensive setup guide (1000+ lines)
✓ Connection test script
✓ Integration examples with AI Employee
✓ Troubleshooting guide
✓ Security recommendations

**To start**: Run `scripts/start_odoo.bat` (Windows) or `./scripts/start_odoo.sh` (Mac/Linux)

**Access**: http://localhost:8069

**Database**: PostgreSQL 15

**Modules**: Invoicing, Accounting, Contacts

**API**: XML-RPC on port 8069

---

**Status**: ✅ READY TO START

**Last Updated**: 2026-02-16

**Version**: Odoo 17 Community Edition

**Docker**: Required (version 29.1.3 detected)

**Next Action**: Start Docker Desktop, then run start script
