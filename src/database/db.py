import json
import os
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
    """Carrega o banco do arquivo JSON. Se nao existir, cria com os dados seed."""
    if not os.path.exists(_DB_FILE):
        _save(_SEED)
        return _SEED
    with open(_DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(db: dict) -> None:
    """Salva o banco no arquivo JSON."""
    with open(_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


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
