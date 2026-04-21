from src.database.db import get_by_id, find_where
from src.helpers.http_response import ok, bad_request, not_found, server_error
from src.helpers.validators import get_path_param

def handler(event, context):
    try:
        treinador_id = get_path_param(event, "id")
        if not treinador_id:
            return bad_request("ID do treinador nao informado")
        
        treinador = get_by_id("treinadores", treinador_id)
        if not treinador:
            return not_found(f"Treinador com ID '{treinador_id}' nao encontrado.")
        
        pokemons = find_where("pokemons", treinador_id=treinador_id)

        resultado = [
            {
                "id": p["id"],
                "nome": p["nome"],
                "tipo": p["tipo"],
                "nivel": p["nivel"],
            }
            for p in pokemons
        ]

        return ok(resultado)
    except Exception as e:
        return server_error(str(e))