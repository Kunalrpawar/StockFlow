def get_api_docs():
    return {
        "title": "StockFlow - Inventory Management System",
        "version": "0.1.0",
        "description": "B2B inventory management platform for tracking products across multiple warehouses",
        "base_url": "http://localhost:5000",
        "endpoints": {
            "health": {
                "path": "GET /health",
                "description": "Health check endpoint",
                "response": {"status": "ok"},
            },
            "create_product": {
                "path": "POST /api/products",
                "description": "Create a new product with initial warehouse inventory",
                "request": {
                    "name": "string (required)",
                    "sku": "string (required, globally unique)",
                    "price": "decimal (required)",
                    "company_id": "integer (required)",
                    "warehouse_id": "integer (required)",
                    "initial_quantity": "integer (default: 0)",
                    "product_type": "string (default: 'standard')",
                    "low_stock_threshold": "integer (optional)",
                },
                "response": {
                    "message": "Product created",
                    "product_id": "integer",
                    "sku": "string",
                },
            },
            "low_stock_alerts": {
                "path": "GET /api/companies/<company_id>/alerts/low-stock",
                "description": "Get low-stock alerts for a company",
                "parameters": {
                    "company_id": "integer (required, in path)",
                },
                "response": {
                    "alerts": [
                        {
                            "product_id": "integer",
                            "product_name": "string",
                            "sku": "string",
                            "warehouse_id": "integer",
                            "warehouse_name": "string",
                            "current_stock": "integer",
                            "threshold": "integer",
                            "days_until_stockout": "integer or null",
                            "supplier": {
                                "id": "integer",
                                "name": "string",
                                "contact_email": "string or null",
                            },
                        }
                    ],
                    "total_alerts": "integer",
                },
            },
        },
    }
