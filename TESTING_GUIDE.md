# Windows PowerShell API Testing Guide

## Quick Test Commands (Copy & Paste in PowerShell)

### 1️⃣ Test Health
```powershell
curl http://localhost:5000/health
```

Expected:
```json
{"status":"ok"}
```

---

### 2️⃣ Get API Documentation
```powershell
curl http://localhost:5000/ | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

Expected: Full JSON with all endpoints

---

### 3️⃣ Create Product (After Database Setup)
```powershell
$body = @{
    name = "Test Widget"
    sku = "TEST-$(Get-Random)"
    price = "49.99"
    company_id = 1
    warehouse_id = 1
    initial_quantity = 50
    product_type = "standard"
    low_stock_threshold = 20
} | ConvertTo-Json

curl -X POST http://localhost:5000/api/products `
    -H "Content-Type: application/json" `
    -Body $body
```

Expected:
```json
{"message":"Product created","product_id":1,"sku":"TEST-12345"}
```

---

### 4️⃣ Get Low-Stock Alerts
```powershell
curl http://localhost:5000/api/companies/1/alerts/low-stock | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

Expected:
```json
{"alerts":[],"total_alerts":0}
```
(Empty until you seed data)

---

## Setup Before Testing

### Terminal 1: Start Server
```powershell
cd c:\Users\Kunal Ramesh Pawar\OneDrive\Desktop\brny
.venv\Scripts\activate
python run.py
```

### Terminal 2: Initialize Database
```powershell
cd c:\Users\Kunal Ramesh Pawar\OneDrive\Desktop\brny
.venv\Scripts\activate
python manage.py init    # Create tables
python manage.py seed    # Add sample data
```

### Terminal 3: Run Tests
```powershell
cd c:\Users\Kunal Ramesh Pawar\OneDrive\Desktop\brny
python verify_api.py
```

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 404 Not Found | Server not running | Start with `python run.py` |
| Connection refused | Wrong port | Check server on http://localhost:5000 |
| 400 Bad Request | Missing fields | Include all required fields in request |
| 409 Conflict | SKU duplicate | Use unique SKU each time |
| 404 Company | Database empty | Run `python manage.py seed` |

---

## Python Script (No curl needed)

If you prefer Python:

```powershell
python verify_api.py
```

This will test all 4 endpoints and show results.

---

## What You Should See

```
======================================================================
STOCKFLOW API VERIFICATION
======================================================================

1️⃣  Testing: GET /health
Status: 200
Response: {"status": "ok"}

2️⃣  Testing: GET /
Status: 200
Title: StockFlow - Inventory Management System
Version: 0.1.0
Endpoints: health, create_product, low_stock_alerts

3️⃣  Testing: POST /api/products
Status: 201
Response: {"message": "Product created", "product_id": 1, ...}

4️⃣  Testing: GET /api/companies/1/alerts/low-stock
Status: 200
Total Alerts: 1

======================================================================
RESULTS
======================================================================
✅ PASS: Health Check
✅ PASS: API Documentation
✅ PASS: Create Product
✅ PASS: Low-Stock Alerts

🎉 ALL TESTS PASSED!
======================================================================
```

---

## Summary

Your API is live at: `http://localhost:5000`

Three endpoints:
- ✅ `GET /health` - Liveness probe
- ✅ `POST /api/products` - Create products (with all fixes!)
- ✅ `GET /api/companies/{id}/alerts/low-stock` - Smart alerts

All documented at: `http://localhost:5000/`
