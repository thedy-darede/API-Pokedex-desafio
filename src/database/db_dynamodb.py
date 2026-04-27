import os
import uuid
import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")

# Nomes das tabelas vêm das variáveis de ambiente do serverless.yml
_TABLES = {
    "treinadores": dynamodb.Table(os.environ["TREINADORES_TABLE"]),
    "pokemons": dynamodb.Table(os.environ["POKEMONS_TABLE"]),
}


def generate_id(table: str = None) -> str:
    return str(uuid.uuid4())


def get_all(table: str) -> list:
    """Equivalente ao seu get_all — faz um Scan na tabela inteira."""
    response = _TABLES[table].scan()
    return response.get("Items", [])


def get_by_id(table: str, id: str):
    """Equivalente ao seu get_by_id — busca por chave primária."""
    response = _TABLES[table].get_item(Key={"id": id})
    return response.get("Item")


def insert(table: str, record: dict) -> dict:
    """Equivalente ao seu insert — cria um item novo."""
    _TABLES[table].put_item(Item=record)
    return record


def update(table: str, id: str, data: dict):
    """Equivalente ao seu update — atualiza campos específicos."""
    # Monta a expressão de update dinamicamente
    expressions = []
    values = {}
    names = {}
    for i, (key, value) in enumerate(data.items()):
        placeholder = f":val{i}"
        name_placeholder = f"#attr{i}"
        expressions.append(f"{name_placeholder} = {placeholder}")
        values[placeholder] = value
        names[name_placeholder] = key

    response = _TABLES[table].update_item(
        Key={"id": id},
        UpdateExpression="SET " + ", ".join(expressions),
        ExpressionAttributeValues=values,
        ExpressionAttributeNames=names,
        ReturnValues="ALL_NEW",
    )
    return response.get("Attributes")


def find_where(table: str, **kwargs) -> list:
    """Equivalente ao seu find_where — filtra por atributos."""
    filter_expr = None
    for key, value in kwargs.items():
        condition = Attr(key).eq(value)
        filter_expr = condition if filter_expr is None else filter_expr & condition

    response = _TABLES[table].scan(FilterExpression=filter_expr)
    return response.get("Items", [])
