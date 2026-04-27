from src.database.db_dynamodb import get_by_id
from src.helpers.http_response import ok, not_found, bad_request, server_error
from src.helpers.validators import get_path_param

def handler(event, context):
    try:
        treinador_id = get_path_param(event, "id")
        if not treinador_id:
            return bad_request("ID do treinador nao informado")
        treinador = get_by_id("treinadores", treinador_id)
        if not treinador:
            return not_found(f"Treinador com ID '{treinador_id}' nao encontrado.")

        return ok(treinador)
    except Exception as e:
        return server_error(str(e))