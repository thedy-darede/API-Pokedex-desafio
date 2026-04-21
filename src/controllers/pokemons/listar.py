from src.database.db import get_all
from src.helpers.http_response import ok, server_error

def handler(event, context):
    try:
        pokemons = get_all("pokemons")
        return ok(pokemons)
    except Exception as e:
        return server_error(str(e))