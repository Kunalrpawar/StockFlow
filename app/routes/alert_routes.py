from flask import Blueprint

from app.models.company import Company
from app.services.alert_service import AlertService
from app.utils.http import error_response, success_response


alert_bp = Blueprint("alert_routes", __name__)


@alert_bp.get("/api/companies/<int:company_id>/alerts/low-stock")
def get_low_stock_alerts(company_id: int):
    company = Company.query.get(company_id)
    if company is None:
        return error_response("Company not found", 404)

    payload = AlertService.get_low_stock_alerts(company_id)
    return success_response(payload, 200)
