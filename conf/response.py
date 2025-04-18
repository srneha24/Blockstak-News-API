import json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


async def custom_request_validation_exception_handler(_request, exc):
    """Custom handler for request validation exceptions."""
    error_message = "Validation Error!"
    error_detail = exc.errors()

    if isinstance(error_detail, list):
        error_key = []
        for error in error_detail:
            if error.get("loc") and f"{error.get('loc')[-1]}" not in error_key:
                error_key.append(f"{error.get('loc')[-1]}")
                error_message += f" '{error.get('loc')[-1]}' {error.get('msg')} !"
    response_data = {
        "success": False,
        "message": error_message,
        "detail": jsonable_encoder(error_detail),
        "data": None,
    }
    return JSONResponse(content=jsonable_encoder(response_data), status_code=400)


async def custom_validation_error_handler(_request, exc):
    """Custom handler for validation errors."""
    error_message = "Validation Error!"
    error_detail = {"source": exc.title, "description": json.loads(exc.json())}
    response_data = {"message": error_message, "detail": error_detail, "data": None}
    return CustomJSONResponse(content=jsonable_encoder(response_data), status_code=400)


async def custom_http_exception_handler(_request, exc):
    """Custom handler for HTTP exceptions."""
    response_data = {"success": False, "message": exc.detail, "data": None}
    return JSONResponse(
        content=jsonable_encoder(response_data), status_code=exc.status_code
    )


class CustomJSONResponse(JSONResponse):
    """Custom JSON response class to handle API responses.
    It formats the response in a consistent way, including success status, message, and data.
    It also allows for custom status codes and messages.
    """
    def __init__(self, content, message: str = None, status_code: int = 200, **kwargs):
        self.message = message
        super().__init__(content=content, status_code=status_code, **kwargs)

    def render(self, content):
        is_success = 200 <= self.status_code < 300
        custom_content = {
            "success": is_success,
            "message": self.message
            or (is_success and "Request Success")
            or "Request Failed",
        }
        if isinstance(content, dict) and "data" in content.keys():
            custom_content.update(**content)
        else:
            custom_content["data"] = content
        if isinstance(custom_content.get("data"), dict) \
            and custom_content.get("data", {}).get("message"):
            custom_content["message"] = custom_content["data"]["message"]
        return super().render(custom_content)
