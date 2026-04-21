from src.database.db import get_by_id
from src.helpers.http_response import ok, not_found, bad_request, server_error
from src.helpers.validators import get_path_param

def handler(event, context):
    try:
        pokemon_id = get_path_param(event, "id")
        if not pokemon_id:
            return bad_request("ID do pokemon nao informado.")
        
        pokemon = get_by_id("pokemons", pokemon_id)
        if not pokemon:
            return not_found(f"Pokemon com ID '{pokemon_id}' nao encontrado.")

        return ok(pokemon)

    except Exception as e:
        return server_error(str(e))
