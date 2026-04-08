from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError

from app.services.product_service import ProductService, ProductServiceError
from app.utils.http import error_response, success_response
from app.utils.validators import ValidationError, validate_create_product_payload


product_bp = Blueprint("product_routes", __name__)


@product_bp.post("/api/products")
def create_product():
    try:
        payload = validate_create_product_payload(request.get_json(silent=True) or {})
        product = ProductService.create_product(payload)
        return success_response(
            {
                "message": "Product created",
                "product_id": product.id,
                "sku": product.sku,
            },
            201,
        )
    except ValidationError as exc:
        return error_response(str(exc), 400)
    except ProductServiceError as exc:
        return error_response(str(exc), 409)
    except SQLAlchemyError:
        return error_response("Database error while creating product", 500)
    except Exception:
        return error_response("Unexpected server error", 500)
