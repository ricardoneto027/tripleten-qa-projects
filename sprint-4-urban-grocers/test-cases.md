# Testes de API — Urban Grocers

Testes realizados com Postman sobre a API do Urban Grocers durante o Sprint 4 do bootcamp TripleTen.  
A collection completa está disponível no ficheiro `TripleTen_postman_collection.json`.

---

## Sumário

| Endpoint | Método | Casos testados | Aprovados | Reprovados |
|---|---|---|---|---|
| `/api/v1/kits/:id/products` | POST | 7 | 5 | 2 |
| `/order-and-go/v1/delivery` | POST | 14 | 9 | 5 |
| **Total** | | **21** | **14** | **7** |

---

## POST /api/v1/kits/:id/products — Adicionar produtos a um kit

| ID | Título | Dados enviados | Resultado esperado | Resultado real | Status | Bug |
|---|---|---|---|---|---|---|
| TC-01 | Adicionar 1 produto existente a um kit existente | `productsList: [{id: 1, quantity: 1}]` no kit 6 | 200 OK | 200 OK | ✅ APROVADO | |
| TC-02 | Adicionar produtos com lista resultante de 30 distintos | 17 produtos novos no kit 6 (que já tinha 13) | 200 OK | 200 OK | ✅ APROVADO | |
| TC-03 | Adicionar produtos com lista resultante de 31 distintos (acima do limite) | Produtos que ultrapassam 30 distintos no kit 6 | 400 Bad Request | 400 Bad Request | ✅ APROVADO | |
| TC-04 | Adicionar produtos com lista resultante de 29 distintos | 29 produtos no kit 8 | 200 OK | 200 OK | ✅ APROVADO | |
| TC-05 | Adicionar produtos a um kit com ID inexistente | `productsList: [{id: 1, quantity: 1}]` no kit 9999 | 404 Not Found | 404 Not Found | ✅ APROVADO | |
| TC-06 | Adicionar produtos sem o campo `productsList` no body | `{}` | 400 Bad Request | 200 OK | ❌ REPROVADO | [PS4TDA-1](https://ricardoneto027.atlassian.net/browse/PS4TDA-1) |
| TC-07 | Adicionar produtos com `productsList` vazia | `productsList: []` | 400 Bad Request | 200 OK | ❌ REPROVADO | [PS4TDA-2](https://ricardoneto027.atlassian.net/browse/PS4TDA-2) |

---

## POST /order-and-go/v1/delivery — Verificar custo e disponibilidade de entrega "Order and Go"

### Validação do campo `productsCount`

| ID | Título | Dados enviados | Resultado esperado | Resultado real | Status | Bug |
|---|---|---|---|---|---|---|
| TC-08 | `productsCount` mínimo válido Tier 1 — valor 0 | `productsCount: 0, productsWeight: 1, deliveryTime: 20` | 200 OK, `hostDeliveryCost: 3, clientDeliveryCost: 0` | 200 OK, `hostDeliveryCost: 3, clientDeliveryCost: 0` | ✅ APROVADO | |
| TC-09 | `productsCount` limite superior Tier 1 — valor 8 | `productsCount: 8, productsWeight: 1, deliveryTime: 20` | 200 OK, `hostDeliveryCost: 3, clientDeliveryCost: 0` | 200 OK, `hostDeliveryCost: 3, clientDeliveryCost: 0` | ✅ APROVADO | |
| TC-10 | `productsCount` limite inferior Tier 2 — valor 9 | `productsCount: 9, productsWeight: 1, deliveryTime: 20` | 200 OK, `hostDeliveryCost: 5, clientDeliveryCost: 0` | 200 OK, `hostDeliveryCost: 5, clientDeliveryCost: 0` | ✅ APROVADO | |
| TC-11 | `productsCount` limite superior Tier 2 — valor 15 | `productsCount: 15, productsWeight: 1, deliveryTime: 20` | 200 OK, `hostDeliveryCost: 5, clientDeliveryCost: 0` | 200 OK, `hostDeliveryCost: 5, clientDeliveryCost: 0` | ✅ APROVADO | |
| TC-12 | `productsCount` acima do máximo Tier 2 — valor 16 | `productsCount: 16, productsWeight: 1, deliveryTime: 20` | 200 OK, `clientDeliveryCost: 9` | 200 OK, `clientDeliveryCost: 5` | ❌ REPROVADO | [PS4TDA-3](https://ricardoneto027.atlassian.net/browse/PS4TDA-3) |

### Validação do campo `productsWeight`

| ID | Título | Dados enviados | Resultado esperado | Resultado real | Status | Bug |
|---|---|---|---|---|---|---|
| TC-13 | `productsWeight` mínimo válido Tier 1 — valor 0kg | `productsCount: 1, productsWeight: 0, deliveryTime: 20` | 200 OK, `hostDeliveryCost: 3, clientDeliveryCost: 0` | 200 OK, `hostDeliveryCost: 3, clientDeliveryCost: 0` | ✅ APROVADO | |
| TC-14 | `productsWeight` limite superior Tier 1 — valor 3kg | `productsCount: 1, productsWeight: 3, deliveryTime: 20` | 200 OK, `hostDeliveryCost: 3, clientDeliveryCost: 0` | 200 OK, `hostDeliveryCost: 3, clientDeliveryCost: 0` | ✅ APROVADO | |
| TC-15 | `productsWeight` limite inferior Tier 2 — valor 3.1kg | `productsCount: 1, productsWeight: 3.1, deliveryTime: 20` | 200 OK, `hostDeliveryCost: 5` | 200 OK, `hostDeliveryCost: 3` | ❌ REPROVADO | [PS4TDA-4](https://ricardoneto027.atlassian.net/browse/PS4TDA-4) |
| TC-16 | `productsWeight` limite superior Tier 2 — valor 6kg | `productsCount: 1, productsWeight: 6, deliveryTime: 20` | 200 OK, `hostDeliveryCost: 5, clientDeliveryCost: 0` | 200 OK, `hostDeliveryCost: 5, clientDeliveryCost: 0` | ✅ APROVADO | |
| TC-17 | `productsWeight` acima do máximo Tier 2 — valor 6.1kg | `productsCount: 1, productsWeight: 6.1, deliveryTime: 20` | 200 OK, `clientDeliveryCost: 9` | 200 OK, `clientDeliveryCost: 0` | ❌ REPROVADO | [PS4TDA-5](https://ricardoneto027.atlassian.net/browse/PS4TDA-5) |

### Validação do campo `deliveryTime`

| ID | Título | Dados enviados | Resultado esperado | Resultado real | Status | Bug |
|---|---|---|---|---|---|---|
| TC-18 | `deliveryTime` abaixo do horário válido — valor 7 | `productsCount: 1, productsWeight: 1, deliveryTime: 7` | 200 OK, `isItPossibleToDeliver: false` | 200 OK, `isItPossibleToDeliver: true` | ❌ REPROVADO | [PS4TDA-6](https://ricardoneto027.atlassian.net/browse/PS4TDA-6) |
| TC-19 | `deliveryTime` limite inferior válido — valor 8 | `productsCount: 1, productsWeight: 1, deliveryTime: 8` | 200 OK, `isItPossibleToDeliver: true` | 200 OK, `isItPossibleToDeliver: true` | ✅ APROVADO | |
| TC-20 | `deliveryTime` limite superior válido — valor 22 | `productsCount: 1, productsWeight: 1, deliveryTime: 22` | 200 OK, `isItPossibleToDeliver: true` | 200 OK, `isItPossibleToDeliver: true` | ✅ APROVADO | |
| TC-21 | `deliveryTime` acima do horário válido — valor 23 | `productsCount: 1, productsWeight: 1, deliveryTime: 23` | 200 OK, `isItPossibleToDeliver: false` | 200 OK, `isItPossibleToDeliver: true` | ❌ REPROVADO | [PS4TDA-7](https://ricardoneto027.atlassian.net/browse/PS4TDA-7) |

---

## Bugs encontrados

| ID | Endpoint | Descrição | Link |
|---|---|---|---|
| PS4TDA-1 | POST /api/v1/kits/:id/products | API aceita body sem campo `productsList` e retorna 200 em vez de 400 | [ver bug](https://ricardoneto027.atlassian.net/browse/PS4TDA-1) |
| PS4TDA-2 | POST /api/v1/kits/:id/products | API aceita `productsList` vazia e retorna 200 em vez de 400 | [ver bug](https://ricardoneto027.atlassian.net/browse/PS4TDA-2) |
| PS4TDA-3 | POST /order-and-go/v1/delivery | `clientDeliveryCost` incorreto para `productsCount: 16` — retorna 5 em vez de 9 | [ver bug](https://ricardoneto027.atlassian.net/browse/PS4TDA-3) |
| PS4TDA-4 | POST /order-and-go/v1/delivery | `hostDeliveryCost` incorreto para `productsWeight: 3.1kg` — retorna 3 em vez de 5 | [ver bug](https://ricardoneto027.atlassian.net/browse/PS4TDA-4) |
| PS4TDA-5 | POST /order-and-go/v1/delivery | `clientDeliveryCost` incorreto para `productsWeight: 6.1kg` — retorna 0 em vez de 9 | [ver bug](https://ricardoneto027.atlassian.net/browse/PS4TDA-5) |
| PS4TDA-6 | POST /order-and-go/v1/delivery | `isItPossibleToDeliver` retorna `true` para `deliveryTime: 7` quando devia ser `false` | [ver bug](https://ricardoneto027.atlassian.net/browse/PS4TDA-6) |
| PS4TDA-7 | POST /order-and-go/v1/delivery | `isItPossibleToDeliver` retorna `true` para `deliveryTime: 23` quando devia ser `false` | [ver bug](https://ricardoneto027.atlassian.net/browse/PS4TDA-7) |

---

## Ferramentas utilizadas

- **Postman** — execução dos testes
- **Jira** — registo de bugs
- **Urban Grocers API** — ambiente de testes TripleTen
