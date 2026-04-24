import json


def parse_body(event: dict) -> tuple:
    """
    Extrai e faz o parse do body da requisicao.
    Retorna (dados, erro). Se erro for None, dados e valido.
    """
    raw = event.get("body") or "{}"
    try:
        if isinstance(raw, str):
            raw = raw.encode("utf-8", errors="replace").decode("utf-8")
        data = json.loads(raw)
        if not isinstance(data, dict):
            return None, "O corpo da requisicao deve ser um objeto JSON."
        return data, None
    except (json.JSONDecodeError, TypeError):
        return None, "Corpo da requisicao invalido. Envie um JSON valido."


def get_path_param(event: dict, param: str):
    """
    Extrai um path parameter do evento e converte para int se possivel.
    Ex: /treinadores/{id} -> get_path_param(event, "id")
    """
    try:
        value = event["pathParameters"][param]
        try:
            return int(value)
        except (ValueError, TypeError):
            return value
    except (KeyError, TypeError):
        return None


def validate_treinador(data: dict) -> str | None:
    """
    Valida os campos de um treinador.
    Retorna mensagem de erro ou None se valido.
    """
    nome = data.get("nome", "")
    if not nome or not isinstance(nome, str) or not nome.strip():
        return "O campo 'nome' e obrigatorio e deve ser uma string nao vazia."
    return None


def validate_pokemon(data: dict) -> str | None:
    """
    Valida os campos de um pokemon no cadastro.
    Retorna mensagem de erro ou None se valido.
    """
    nome = data.get("nome", "")
    if not nome or not isinstance(nome, str) or not nome.strip():
        return "O campo 'nome' e obrigatorio."

    tipo = data.get("tipo", "")
    if not tipo or not isinstance(tipo, str) or not tipo.strip():
        return "O campo 'tipo' e obrigatorio."

    nivel = data.get("nivel")
    if nivel is None:
        return "O campo 'nivel' e obrigatorio."
    if not isinstance(nivel, int) or nivel < 1:
        return "O campo 'nivel' deve ser um inteiro maior ou igual a 1."

    treinador_id = data.get("treinador_id")
    if treinador_id is None:
        return "O campo 'treinador_id' e obrigatorio."
    if not isinstance(treinador_id, int):
        return "O campo 'treinador_id' deve ser um numero inteiro."

    return None


def validate_pokemon_update(data: dict) -> str | None:
    """
    Valida os campos de um pokemon na atualizacao.
    Todos os campos sao opcionais, mas devem ser validos se presentes.
    """
    if "nome" in data:
        nome = data["nome"]
        if not nome or not isinstance(nome, str) or not nome.strip():
            return "O campo 'nome' deve ser uma string nao vazia."

    if "tipo" in data:
        tipo = data["tipo"]
        if not tipo or not isinstance(tipo, str) or not tipo.strip():
            return "O campo 'tipo' deve ser uma string nao vazia."

    if "nivel" in data:
        nivel = data["nivel"]
        if not isinstance(nivel, int) or nivel < 1:
            return "O campo 'nivel' deve ser um inteiro maior ou igual a 1."

    return None