from src.database.db import get_all
from src.helpers.http_response import ok, server_error

def handler(event, context):
    try:
        treinadores = get_all("treinadores")
        return ok(treinadores)
    except Exception as e:
        return server_error(str(e))