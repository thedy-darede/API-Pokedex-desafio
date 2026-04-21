from src.database.db import insert, generate_id
from src.helpers.http_response import created, bad_request, server_error
from src.helpers.validators import parse_body, validate_treinador

def handler(event, context):
    try:
        data, err = parse_body(event)
        if err:
            return bad_request(err)
            
        err = validate_treinador(data)
        if err:
            return bad_request(err)

        treinador = {
            "id": generate_id(),
            "nome": data["nome"].strip(),
        }

        insert("treinadores", treinador)

        return created(treinador)
    except Exception as e:
        return server_error(str(e))