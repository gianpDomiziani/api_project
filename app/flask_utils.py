import json

from flask import Response

def build_json_response(body: str, http_status: int, api_method: str) -> Response:
        json_body = json.dumps(body, indent=4, sort_keys=False)

        response = Response(
            response = json_body,
            status = http_status,
            mimetype="application/json",
            headers = {"API method": api_method}
        )
        return response

def build_error_response(error: str, api_method: str) -> Response:

    return build_json_response(body={"error": [error]}, http_status=400, api_method=api_method)

