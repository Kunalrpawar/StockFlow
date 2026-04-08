"""
Test suite for API endpoints using curl commands.
You can run these manually in your terminal to verify the API works.
"""

TEST_COMMANDS = {
    "health": {
        "description": "Test health endpoint",
        "cmd": 'curl -X GET http://localhost:5000/health',
    },
    "api_root": {
        "description": "Get API documentation",
        "cmd": 'curl -X GET http://localhost:5000/',
    },
    "create_product_example": {
        "description": "Create a test product",
        "cmd": '''curl -X POST http://localhost:5000/api/products \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Test Widget",
    "sku": "TEST-001",
    "price": "29.99",
    "company_id": 1,
    "warehouse_id": 1,
    "initial_quantity": 50,
    "product_type": "standard",
    "low_stock_threshold": 20
  }' ''',
    },
    "get_alerts_example": {
        "description": "Get low-stock alerts for company 1",
        "cmd": 'curl -X GET http://localhost:5000/api/companies/1/alerts/low-stock',
    },
}


def print_curl_commands():
    """Print all test curl commands."""
    print("\n" + "=" * 70)
    print("STOCKFLOW API TEST COMMANDS")
    print("=" * 70 + "\n")

    for test_name, test_info in TEST_COMMANDS.items():
        print(f"Test: {test_name}")
        print(f"Description: {test_info['description']}")
        print(f"Command:\n{test_info['cmd']}\n")
        print("-" * 70 + "\n")


if __name__ == "__main__":
    print_curl_commands()
