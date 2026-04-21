from src.database.db import update, get_by_id
from src.helpers.http_response import ok, bad_request, not_found, server_error
from src.helpers.validators import parse_body, validate_treinador, get_path_param


def handler(event, context):
    try:
        treinador_id = get_path_param(event, "id")
        if not treinador_id:
            return bad_request("ID do treinador nao informado.")
        
        treinador = get_by_id("treinadores", treinador_id)
        if not treinador:
            return not_found(f"Treinador com id '{treinador_id}' nao encontrado.")

        data, err = parse_body(event)
        if err:
            return bad_request(err)

        err = validate_treinador(data)
        if err:
            return bad_request(err)

        treinador_atualizado = update("treinadores", treinador_id, {
            "nome": data["nome"].strip(),
        })

        return ok(treinador_atualizado)
    except Exception as e:
        return server_error(str(e))