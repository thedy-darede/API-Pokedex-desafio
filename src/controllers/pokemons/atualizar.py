from src.database.db import update, get_by_id
from src.helpers.http_response import ok, bad_request, not_found, server_error
from src.helpers.validators import parse_body, validate_pokemon_update, get_path_param

def handler(event, context):
    try:
        pokemon_id = get_path_param(event, "id")
        if not pokemon_id:
            return bad_request("ID do pokemon nao informado")

        pokemon = get_by_id("pokemons", pokemon_id)
        if not pokemon:
            return not_found(f"Pokemon com ID '{pokemon_id}' nao encontrado")

        data, err = parse_body(event)
        if err:
            return bad_request(err)

        err = validate_pokemon_update(data)
        if err:
            return bad_request(err)

        campos_permitidos = {"nome", "tipo", "nivel"}
        payload = {}
        for campo in campos_permitidos:
            if campo in data:
                valor = data[campo]
                payload[campo] = valor.strip() if isinstance(valor, str) else valor

        if not payload:
            return bad_request("Nenhum campo valido para atualizacao foi informado")

        pokemon_atualizado = update("pokemons", pokemon_id, payload)

        return ok(pokemon_atualizado)

    except Exception as e:
        return server_error(str(e))