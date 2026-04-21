# Desafio API Pokédex — Diário de Progresso

## Visão Geral
API REST com Serverless Framework (Python 3.11) para gerenciar treinadores, pokémons e batalhas.

---

## Status dos Endpoints

### Treinadores
| Endpoint | Handler | Status |
|---|---|---|
| `GET /treinadores` | `listar.py` | ✅ Criado |
| `GET /treinadores/{id}` | `buscar.py` | ✅ Criado |
| `POST /treinadores` | `cadastrar.py` | ✅ Criado |
| `PUT /treinadores/{id}` | `atualizar.py` | ✅ Criado |
| `GET /treinadores/{id}/pokemons` | `listar_pokemons.py` | ✅ Criado |

### Pokémons
| Endpoint | Handler | Status |
|---|---|---|
| `GET /pokemons` | `listar.py` | ✅ Criado |
| `GET /pokemons/{id}` | `buscar.py` | ✅ Criado |
| `POST /pokemons` | `cadastrar.py` | ✅ Criado |
| `PUT /pokemons/{id}` | `atualizar.py` | ✅ Criado |

### Batalhas
| Endpoint | Handler | Status |
|---|---|---|
| `POST /batalhas` | `batalhar.py` | ❌ Não criado |

---

## Módulos Auxiliares

| Módulo | Status | Observação |
|---|---|---|
| `src/database/db.py` | ✅ Completo | Banco in-memory com lock, dados seed de exemplo |
| `src/helpers/http_response.py` | ✅ Completo | Respostas padronizadas (200, 201, 400, 404, 422, 500) |
| `src/helpers/validators.py` | ✅ Completo | Validações para treinador, pokémon e pokémon update |

---

## Bugs Encontrados

### ~~Bug 1 — `buscar.py`: typo no nome da variável~~ ✅ Corrigido
Typo `treinado_id` → `treinador_id`

### ~~Bug 2 — `cadastrar.py`: `generate_id` sem parênteses~~ ✅ Corrigido
`generate_id` → `generate_id()`

### ~~Bug 3 — `atualizar.py`: typo `treinado_id`~~ ✅ Corrigido
`treinado_id` → `treinador_id` (linhas 14 e 23)

### ~~Bug 4 — `listar_pokemons.py`: imports errados + typo~~ ✅ Corrigido
- `src.handlers` → `src.helpers` (linhas 2-3)
- `treinado_id` → `treinador_id` (linha 15)

### ~~Bug 5 — `pokemons/cadastrar.py`: 3 erros~~ ✅ Corrigido
- Import `create` → `created`
- Tabela `"treinador"` → `"treinadores"`
- Aspas aninhadas na f-string

### ~~Bug 6 — `pokemons/atualizar.py`: 2 erros~~ ✅ Corrigido
- Typo `pokemom` → `pokemon`
- `instance()` → `isinstance()`

---

## Problemas de Configuração (pendentes da análise anterior)

### 1. Versão do Serverless inconsistente
- `package.json` usa `serverless: ^4.34.0`
- `serverless.yml` tem `frameworkVersion: '3'`
- **Ação:** Alinhar para a mesma versão

### 2. `requirements.txt` sem dependências de runtime
- Só tem `pytest`, `pytest-mock`, `requests` (dependências de teste)
- Se for usar AWS (DynamoDB, etc.), adicionar `boto3`

### 3. Pasta de testes `teste/`
- `pytest` procura por `tests/` ou `test/` por padrão
- Considerar renomear ou configurar `pytest.ini`

---

## Próximos Passos
1. [x] ~~Corrigir Bug 1 — typo em `buscar.py`~~
2. [x] ~~Corrigir Bug 2 — parênteses em `cadastrar.py`~~
3. [x] ~~Criar `atualizar.py` para treinadores~~
4. [x] ~~Criar `listar_pokemons.py` para treinadores~~
5. [x] ~~Criar handlers de pokémons (listar, buscar, cadastrar, atualizar)~~
6. [ ] Criar handler de batalhas
7. [ ] Resolver inconsistência de versão do Serverless
8. [ ] Adicionar testes
9. [ ] Configurar pytest para pasta `teste/`

---

*Última atualização: 21/04/2026*
