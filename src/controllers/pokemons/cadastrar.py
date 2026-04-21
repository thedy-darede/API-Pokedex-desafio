from src.database.db import insert, generate_id, get_by_id
from src.helpers.http_response import created, bad_request, not_found, server_error
from src.helpers.validators import parse_body, validate_pokemon

def handler(event, context):
    try:
        data, err = parse_body(event)
        if err:
            return bad_request(err)

        err = validate_pokemon(data)
        if err:
            return bad_request(err)

        treinador = get_by_id("treinadores", data["treinador_id"])
        if not treinador:
            return not_found(f"Treinador com ID '{data['treinador_id']}' nao encontrado.")
        

        pokemon = {
            "id": generate_id(),
            "nome": data["nome"].strip(),
            "tipo": data["tipo"].strip(),
            "nivel": data["nivel"],
            "treinador_id": data["treinador_id"],
        }

        insert("pokemons", pokemon)

        return created(pokemon)
    except Exception as e:
        return server_error(str(e))
