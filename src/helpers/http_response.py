import json
from decimal import Decimal


class _DecimalEncoder(json.JSONEncoder):
    """Converte Decimal do DynamoDB para int ou float."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj == int(obj) else float(obj)
        return super().default(obj)


def _build_response(status_code: int, body) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, ensure_ascii=False, cls=_DecimalEncoder),
    }


def ok(body) -> dict:
    return _build_response(200, body)


def created(body) -> dict:
    return _build_response(201, body)


def bad_request(message: str) -> dict:
    return _build_response(400, {"erro": message})


def not_found(message: str = "Recurso nao encontrado") -> dict:
    return _build_response(404, {"erro": message})


def unprocessable(message: str) -> dict:
    return _build_response(422, {"erro": message})


def server_error(message: str = "Erro interno do servidor") -> dict:
    return _build_response(500, {"erro": message})

