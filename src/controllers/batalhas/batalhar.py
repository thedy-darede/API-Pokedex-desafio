from src.database.db import get_by_id
from src.helpers.http_response import ok, bad_request, not_found, unprocessable, server_error
from src.helpers.validators import parse_body
import unicodedata

_VANTAGENS = {
    "fogo": "planta",
    "planta": "agua",
    "agua": "fogo",
}


def _normalizar_tipo(tipo: str) -> str:
    """Normaliza o tipo removendo acentos, espacos e convertendo para minusculo."""
    texto = tipo.strip().lower()
    # Remove acentos: Água -> Agua -> agua
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _determinar_vencedor(atacante: dict, defensor: dict) -> dict:
    # 1) Nivel mais alto vence
    if atacante["nivel"] != defensor["nivel"]:
        if atacante["nivel"] > defensor["nivel"]:
            vencedor, perdedor = atacante, defensor
        else:
            vencedor, perdedor = defensor, atacante

        return {
            "resultado": "vitoria",
            "vencedor": {"id": vencedor["id"], "nome": vencedor["nome"]},
            "perdedor": {"id": perdedor["id"], "nome": perdedor["nome"]},
        }

    # 2) Empate de nivel — tipo decide
    tipo_atk = _normalizar_tipo(atacante["tipo"])
    tipo_def = _normalizar_tipo(defensor["tipo"])

    if _VANTAGENS.get(tipo_atk) == tipo_def:
        return {
            "resultado": "vitoria",
            "vencedor": {"id": atacante["id"], "nome": atacante["nome"]},
            "perdedor": {"id": defensor["id"], "nome": defensor["nome"]},
        }

    if _VANTAGENS.get(tipo_def) == tipo_atk:
        return {
            "resultado": "vitoria",
            "vencedor": {"id": defensor["id"], "nome": defensor["nome"]},
            "perdedor": {"id": atacante["id"], "nome": atacante["nome"]},
        }

    # 3) Mesmo nivel e mesmo tipo (ou sem relacao) — empate
    return {
        "resultado": "empate",
        "mensagem": "Os Pokemon possuem forca equivalente",
    }


def handler(event, context):
    try:
        data, err = parse_body(event)
        if err:
            return bad_request(err)

        atk_id = data.get("pokemon_atacante_id")
        def_id = data.get("pokemon_defensor_id")

        if not atk_id or not def_id:
            return bad_request(
                "Os campos 'pokemon_atacante_id' e 'pokemon_defensor_id' sao obrigatorios."
            )

        if atk_id == def_id:
            return unprocessable("Um Pokemon nao pode batalhar contra ele mesmo.")

        atacante = get_by_id("pokemons", atk_id)
        if not atacante:
            return not_found(f"Pokemon atacante com ID '{atk_id}' nao encontrado.")

        defensor = get_by_id("pokemons", def_id)
        if not defensor:
            return not_found(f"Pokemon defensor com ID '{def_id}' nao encontrado.")

        if atacante["nome"].strip().lower() == defensor["nome"].strip().lower():
            return unprocessable("Um Pokemon nao pode batalhar contra outro de mesma especie.")

        resultado = _determinar_vencedor(atacante, defensor)
        return ok(resultado)
    except Exception as e:
        return server_error(str(e))