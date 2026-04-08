#!/usr/bin/env python
"""
Quick API endpoint verification script.
Tests all three endpoints with sample data.
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint."""
    print("\n1️⃣  Testing: GET /health")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_api_docs():
    """Test API documentation endpoint."""
    print("\n2️⃣  Testing: GET /")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Title: {data.get('title')}")
    print(f"Version: {data.get('version')}")
    print(f"Endpoints: {', '.join(data.get('endpoints', {}).keys())}")
    return response.status_code == 200


def test_create_product():
    """Test product creation endpoint."""
    print("\n3️⃣  Testing: POST /api/products")
    
    payload = {
        "name": "Test Widget",
        "sku": f"TEST-{hash('widget')% 10000}",
        "price": "49.99",
        "company_id": 1,
        "warehouse_id": 1,
        "initial_quantity": 50,
        "product_type": "standard",
        "low_stock_threshold": 20
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    response = requests.post(f"{BASE_URL}/api/products", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201


def test_low_stock_alerts():
    """Test low-stock alerts endpoint."""
    print("\n4️⃣  Testing: GET /api/companies/1/alerts/low-stock")
    response = requests.get(f"{BASE_URL}/api/companies/1/alerts/low-stock")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total Alerts: {data.get('total_alerts')}")
    if data.get('alerts'):
        print(f"Sample Alert: {json.dumps(data['alerts'][0], indent=2)}")
    else:
        print("No alerts found")
    return response.status_code == 200


if __name__ == "__main__":
    print("=" * 70)
    print("STOCKFLOW API VERIFICATION")
    print("=" * 70)
    
    results = {
        "Health Check": test_health(),
        "API Documentation": test_api_docs(),
        "Create Product": test_create_product(),
        "Low-Stock Alerts": test_low_stock_alerts(),
    }
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    print("\n" + ("🎉 ALL TESTS PASSED!" if all_passed else "⚠️  SOME TESTS FAILED"))
    print("=" * 70)
