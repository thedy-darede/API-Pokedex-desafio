import json
import os
import tempfile
import uuid
from threading import Lock

_lock = Lock()

_DB_FILE = os.path.join(os.path.dirname(__file__), "data.json")

_SEED = {
    "treinadores": {
        "ash-001": {"id": "ash-001", "nome": "Ash"},
        "misty-002": {"id": "misty-002", "nome": "Misty"},
    },
    "pokemons": {
        "pika-001": {"id": "pika-001", "nome": "Pikachu", "tipo": "Eletrico", "nivel": 10, "treinador_id": "ash-001"},
        "bulb-002": {"id": "bulb-002", "nome": "Bulbasaur", "tipo": "Planta", "nivel": 7, "treinador_id": "ash-001"},
        "star-003": {"id": "star-003", "nome": "Starmie", "tipo": "Agua", "nivel": 9, "treinador_id": "misty-002"},
    },
}


def _load() -> dict:
    """Carrega o banco do arquivo JSON. Se nao existir ou estiver corrompido, recria com seed."""
    if not os.path.exists(_DB_FILE):
        _save(_SEED)
        return json.loads(json.dumps(_SEED))
    try:
        with open(_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        _save(_SEED)
        return json.loads(json.dumps(_SEED))


def _sanitize(obj):
    """Remove surrogates invalidos de strings para evitar erros de encoding."""
    if isinstance(obj, str):
        return obj.encode("utf-8", errors="replace").decode("utf-8")
    if isinstance(obj, dict):
        return {_sanitize(k): _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(item) for item in obj]
    return obj


def _save(db: dict) -> None:
    """Salva o banco no arquivo JSON com escrita atomica."""
    db = _sanitize(db)
    dir_name = os.path.dirname(_DB_FILE)
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, _DB_FILE)
    except BaseException:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def generate_id() -> str:
    return str(uuid.uuid4())


def get_all(table: str) -> list:
    with _lock:
        db = _load()
        return list(db[table].values())


def get_by_id(table: str, id: str):
    with _lock:
        db = _load()
        return db[table].get(id)


def insert(table: str, record: dict) -> dict:
    with _lock:
        db = _load()
        db[table][record["id"]] = record
        _save(db)
        return record


def update(table: str, id: str, data: dict):
    with _lock:
        db = _load()
        if id not in db[table]:
            return None
        db[table][id].update(data)
        _save(db)
        return db[table][id]


def find_where(table: str, **kwargs) -> list:
    with _lock:
        db = _load()
        result = []
        for record in db[table].values():
            if all(record.get(k) == v for k, v in kwargs.items()):
                result.append(record)
        return result
