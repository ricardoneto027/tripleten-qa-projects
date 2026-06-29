[sprint6-README.md](https://github.com/user-attachments/files/29476021/sprint6-README.md)
# Sprint 6 — Linux, SSH e SQL: Servidor de Táxis de Chicago

Projeto prático em duas partes: análise de logs num servidor remoto via SSH
com comandos Linux, e consultas SQL sobre uma base de dados real de corridas
de táxi de Chicago.

---

## 🖥️ Contexto

| Campo | Detalhe |
|---|---|
| Servidor remoto | `containerhub.tripleten-services.com` |
| Acesso | SSH com autenticação por chave pública |
| Base de dados | `chicago_taxi` (PostgreSQL) |
| Ferramentas | Terminal (macOS), comandos Linux, SQL |

---

## 📁 Estrutura da pasta

| Ficheiro | Descrição |
|---|---|
| `console-tarefa-1.md` | Análise de logs por endereço IP |
| `console-tarefa-2.md` | Isolamento de erros 400 e 500 em ficheiros separados |
| `sql-tarefa-1.md` | Contagem total de táxis na tabela `cabs` |
| `sql-tarefa-2.md` | Empresas com menos de 100 carros (operador `HAVING`) |
| `sql-tarefa-3.md` | Classificação de condições meteorológicas (operador `CASE`) |
| `sql-tarefa-4.md` | Número de corridas por empresa em 15–16 Nov 2017 |

---

## 🔍 Parte 1 — Console (Linux/SSH)

### Tarefa 1 — Análise de logs por IP

Identificação de todas as solicitações enviadas a partir de endereços IP começados
por `233.201.` nos logs do servidor remoto em `logs/2019/12/`.

**Técnicas utilizadas:** `grep -r` com âncora de início de linha (`^`)

### Tarefa 2 — Isolamento de erros 400 e 500

Extração dos logs de 30/12/2019 com erros 400 e 500 para ficheiros separados,
organizados numa estrutura de diretórios criada no servidor remoto.

**Estrutura criada no servidor:**
```
~/bug1/
├── main.txt        ← todos os erros 400 e 500 de 30/12/2019
└── events/
    ├── 400.txt     ← apenas erros 400 (172 linhas)
    └── 500.txt     ← apenas erros 500 (156 linhas)
```

**Técnicas utilizadas:** `grep -E`, redirecionamento de output (`>`), `mkdir`

---

## 🗄️ Parte 2 — SQL (Base de dados chicago_taxi)

### Estrutura da base de dados

```
neighborhoods       cabs                trips                  weather_records
──────────────      ────────────────    ──────────────────     ───────────────
neighborhood_id     cab_id              trip_id                record_id
name                vehicle_id          cab_id                 ts
                    company_name        start_ts               temperature
                                        end_ts                 description
                                        duration_seconds
                                        distance_miles
                                        pickup_location_id
                                        dropoff_location_id
```

> `trips` e `weather_records` relacionam-se por timestamp (`start_ts` = `ts`).

### Tarefa 1 — Total de táxis disponíveis
O plano era ter 10.550 veículos. A consulta revelou **5.529 táxis** — cerca de metade do previsto.

### Tarefa 2 — Empresas com menos de 100 carros
51 empresas identificadas com menos de 100 veículos, usando `HAVING` para filtrar resultados agregados.

### Tarefa 3 — Classificação de condições meteorológicas
24 registos classificados em `Good` / `Bad` para 05/11/2017, usando `CASE WHEN` com `LIKE` para detetar chuva e tempestade.

### Tarefa 4 — Corridas por empresa em 15–16 Nov 2017
64 empresas listadas por volume de corridas, com `JOIN` entre `trips` e `cabs`, filtradas por intervalo de datas.

---

## 🛠️ Comandos e conceitos aplicados

| Área | Conceitos |
|---|---|
| Linux/SSH | Autenticação por chave pública, `grep -r`, `grep -E`, `>`, `mkdir`, `wc`, `head`, `tail` |
| SQL | `COUNT()`, `GROUP BY`, `ORDER BY DESC`, `HAVING`, `CASE WHEN`, `JOIN`, `WHERE BETWEEN` |

---

## ✅ Estado

Projeto submetido e aprovado pela TripleTen.
