from decimal import Decimal, InvalidOperation


class ValidationError(Exception):
    pass


def parse_decimal(value, field_name: str) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValidationError(f"{field_name} must be a valid decimal value") from exc

    if amount < 0:
        raise ValidationError(f"{field_name} must be greater than or equal to 0")
    return amount


def parse_int(value, field_name: str, *, min_value: int | None = None) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field_name} must be an integer") from exc

    if min_value is not None and parsed < min_value:
        raise ValidationError(f"{field_name} must be greater than or equal to {min_value}")
    return parsed


def validate_create_product_payload(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValidationError("JSON body is required")

    required_fields = ["name", "sku", "price", "company_id", "warehouse_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    name = str(data["name"]).strip()
    sku = str(data["sku"]).strip()

    if not name:
        raise ValidationError("name must not be empty")
    if not sku:
        raise ValidationError("sku must not be empty")

    return {
        "name": name,
        "sku": sku,
        "price": parse_decimal(data["price"], "price"),
        "company_id": parse_int(data["company_id"], "company_id", min_value=1),
        "warehouse_id": parse_int(data["warehouse_id"], "warehouse_id", min_value=1),
        "initial_quantity": parse_int(data.get("initial_quantity", 0), "initial_quantity", min_value=0),
        "product_type": str(data.get("product_type", "standard")).strip() or "standard",
        "low_stock_threshold": (
            parse_int(data["low_stock_threshold"], "low_stock_threshold", min_value=0)
            if data.get("low_stock_threshold") is not None
            else None
        ),
    }
