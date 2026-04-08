def success_response(payload: dict, status_code: int = 200):
    return payload, status_code


def error_response(message: str, status_code: int = 400, details: dict | None = None):
    body = {"error": message}
    if details:
        body["details"] = details
    return body, status_code
