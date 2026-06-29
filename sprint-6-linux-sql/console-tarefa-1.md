# Console — Tarefa 1: Análise de logs por endereço IP

**Objetivo:** Identificar todas as solicitações enviadas a partir de endereços IP
começados por `233.201.` nos logs do servidor remoto em `logs/2019/12/`.

---

## Comando utilizado

```bash
grep -r "^233.201." ~/logs/2019/12/
```

**Explicação:**
- `grep` — pesquisa de padrões em ficheiros de texto
- `-r` — pesquisa recursiva em todos os ficheiros do diretório
- `"^233.201."` — padrão com âncora `^` para garantir que o IP está no início da linha
- `~/logs/2019/12/` — diretório com os logs de dezembro de 2019

---

## Resultados

```
233.201.188.154 - - [18/12/2019:21:46:01 +0000] "DELETE /events HTTP/1.1" 403 3971
233.201.182.9 - - [21/12/2019:21:56:20 +0000] "PATCH /users HTTP/1.1" 400 4118
```

**Análise dos resultados:**

| IP | Data | Método | Endpoint | Status |
|---|---|---|---|---|
| 233.201.188.154 | 18/12/2019 21:46:01 | DELETE | /events | 403 |
| 233.201.182.9 | 21/12/2019 21:56:20 | PATCH | /users | 400 |

Foram encontradas 2 solicitações provenientes do intervalo de IP `233.201.*` nos logs de dezembro de 2019.
