import uuid
from threading import Lock

_lock = Lock()

_db = {
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


def generate_id() -> str:
    return str(uuid.uuid4())


def get_all(table: str) -> list:
    with _lock:
        return list(_db[table].values())


def get_by_id(table: str, id: str):
    with _lock:
        return _db[table].get(id)


def insert(table: str, record: dict) -> dict:
    with _lock:
        _db[table][record["id"]] = record
        return record


def update(table: str, id: str, data: dict):
    with _lock:
        if id not in _db[table]:
            return None
        _db[table][id].update(data)
        return _db[table][id]


def find_where(table: str, **kwargs) -> list:
    with _lock:
        result = []
        for record in _db[table].values():
            if all(record.get(k) == v for k, v in kwargs.items()):
                result.append(record)
        return result