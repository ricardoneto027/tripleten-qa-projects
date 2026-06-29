# Console — Tarefa 2: Isolamento de erros 400 e 500

**Objetivo:** Extrair os logs de 30/12/2019 com erros 400 e 500 para ficheiros
separados, organizados numa estrutura de diretórios no servidor remoto.

---

## Passo 1 — Criar estrutura de diretórios

```bash
mkdir ~/bug1
mkdir ~/bug1/events
```

---

## Passo 2 — Extrair todos os erros 400 e 500 para main.txt

```bash
grep -E " (400|500) " ~/logs/2019/12/apache_2019-12-30.txt > ~/bug1/main.txt
```

**Explicação:**
- `grep -E` — modo de expressão regular estendida
- `" (400|500) "` — filtra linhas com código de status 400 ou 500 (com espaços para evitar falsos positivos)
- `>` — redireciona o output para o ficheiro `main.txt`

---

## Passo 3 — Separar erros por tipo

```bash
grep " 400 " ~/bug1/main.txt > ~/bug1/events/400.txt
grep " 500 " ~/bug1/main.txt > ~/bug1/events/500.txt
```

---

## Resultados

### 400.txt — 172 linhas

**Primeiras 3 linhas:**
```
80.57.170.51 - - [30/12/2019:21:35:12 +0000] "DELETE /users HTTP/1.1" 400 3623
204.235.176.118 - - [30/12/2019:21:35:13 +0000] "POST /users HTTP/1.1" 400 4704
82.95.203.67 - - [30/12/2019:21:35:19 +0000] "DELETE /lists HTTP/1.1" 400 3737
```

**Últimas 3 linhas:**
```
203.106.235.105 - - [30/12/2019:22:12:38 +0000] "DELETE /events HTTP/1.1" 400 4158
18.211.28.150 - - [30/12/2019:22:12:40 +0000] "DELETE /collectors HTTP/1.1" 400 2212
229.16.123.45 - - [30/12/2019:22:12:54 +0000] "GET /auth HTTP/1.1" 400 2397
```

### 500.txt — 156 linhas

**Primeiras 3 linhas:**
```
64.250.112.189 - - [30/12/2019:21:35:13 +0000] "PUT /parsers HTTP/1.1" 500 4639
193.253.101.180 - - [30/12/2019:21:35:31 +0000] "PATCH /alerts HTTP/1.1" 500 2944
197.106.117.194 - - [30/12/2019:21:35:31 +0000] "PATCH /parsers HTTP/1.1" 500 3519
```

**Últimas 3 linhas:**
```
207.6.210.203 - - [30/12/2019:22:12:37 +0000] "PATCH /events HTTP/1.1" 500 4298
33.13.118.148 - - [30/12/2019:22:12:38 +0000] "PUT /alerts HTTP/1.1" 500 4711
107.188.33.199 - - [30/12/2019:22:12:59 +0000] "POST /parsers HTTP/1.1" 500 2833
```

---

## Estrutura final criada no servidor

```
~/bug1/
├── main.txt        ← 328 linhas (172 erros 400 + 156 erros 500)
└── events/
    ├── 400.txt     ← 172 linhas
    └── 500.txt     ← 156 linhas
```
