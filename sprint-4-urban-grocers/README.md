## Sprint 4 — API Testing: Urban Grocers

Testes de API realizados sobre o back-end da aplicação **Urban Grocers** utilizando Postman, cobrindo endpoints de criação, consulta e eliminação de recursos.

---

## 🔌 Contexto

| Campo | Detalhe |
|---|---|
| Aplicação | Urban Grocers | Testes de API REST com Postman |
| Tipo de teste | Testes de API REST |
| Ferramenta | Postman |
| Formato de dados | JSON |

---

## 📁 Ficheiros

| Ficheiro | Descrição |
|---|---|
| `urban-scooter.postman_collection.json` | Collection Postman com todos os testes |
| `test-cases.md` | Casos de teste documentados |
| `bug-reports.md` | Bugs encontrados na API |

---

## 🔍 Endpoints testados

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/api/v1/orders` | Listar encomendas |
| POST | `/api/v1/orders` | Criar nova encomenda |
| GET | `/api/v1/orders/:id` | Consultar encomenda por ID |
| DELETE | `/api/v1/orders/:id` | Cancelar encomenda |
| GET | `/api/v1/couriers` | Listar estafetas |

> Adapta com os endpoints reais que testaste.

---

## 🧪 Tipos de testes incluídos

- Testes positivos (happy path)
- Testes negativos (dados inválidos, campos em falta)
- Verificação de status codes
- Validação do corpo da resposta (response body)

---

## ✅ Estado

Projeto submetido e aprovado pela TripleTen.
