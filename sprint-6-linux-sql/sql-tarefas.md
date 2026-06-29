# SQL — Tarefas 1 a 4: Base de dados chicago_taxi

Base de dados PostgreSQL de corridas de táxi de Chicago, acedida via SSH
ao servidor remoto e consultada com `psql`.

**Ligação ao servidor:**
```bash
psql -U morty -d chicago_taxi
# password: smith
```

---

## Tarefa 1 — Total de táxis disponíveis

O plano era ter 10.550 veículos disponíveis. A consulta revelou o número real.

### Consulta

```sql
SELECT COUNT(DISTINCT cab_id) FROM cabs;
```

### Resultado

```
 count
-------
  5529
```

**Conclusão:** Apenas 5.529 táxis estavam nas ruas — aproximadamente metade do planeado, o que justifica as reclamações dos utilizadores.

---

## Tarefa 2 — Empresas com menos de 100 carros

### Consulta

```sql
SELECT company_name,
       COUNT(cab_id) AS cnt
FROM cabs
GROUP BY company_name
HAVING COUNT(cab_id) < 100
ORDER BY cnt DESC;
```

**Conceito aplicado:** `HAVING` filtra resultados após agregação — equivalente ao `WHERE` mas para funções como `COUNT()`.

### Resultado (51 empresas)

```
                 company_name                 | cnt 
----------------------------------------------+-----
 Nova Taxi Affiliation Llc                    |  97
 Patriot Taxi Dba Peace Taxi Associat         |  89
 Blue Diamond                                 |  85
 Checker Taxi Affiliation                     |  81
 Chicago Medallion Management                 |  80
 Chicago Independents                         |  69
 24 Seven Taxi                                |  67
 Checker Taxi                                 |  60
 American United                              |  55
 Chicago Medallion Leasing INC                |  53
 Top Cab Affiliation                          |  49
 KOAM Taxi Association                        |  48
 Chicago Taxicab                              |  38
 Norshore Cab                                 |  34
 Gold Coast Taxi                              |  20
 Metro Group                                  |  20
 Service Taxi Association                     |  18
 5 Star Taxi                                  |  14
 American United Taxi Affiliation             |   8
 Metro Jet Taxi A                             |   8
 Setare Inc                                   |   7
 Leonard Cab Co                               |   5
 [+ 29 empresas com 1 veículo cada]
(51 rows)
```

---

## Tarefa 3 — Classificação de condições meteorológicas

### Consulta

```sql
SELECT ts,
       CASE
           WHEN description LIKE '%rain%' OR description LIKE '%storm%' THEN 'Bad'
           ELSE 'Good'
       END AS weather_conditions
FROM weather_records
WHERE ts BETWEEN '2017-11-05 00:00:00' AND '2017-11-05 23:59:59';
```

**Conceito aplicado:** `CASE WHEN ... THEN ... ELSE ... END` para lógica condicional. `LIKE '%rain%'` deteta a palavra em qualquer posição da descrição.

### Resultado

```
         ts          | weather_conditions 
---------------------+--------------------
 2017-11-05 00:00:00 | Good
 2017-11-05 01:00:00 | Bad
 2017-11-05 02:00:00 | Good
 2017-11-05 03:00:00 | Good
 2017-11-05 04:00:00 | Bad
 2017-11-05 05:00:00 | Bad
 2017-11-05 06:00:00 | Good
 2017-11-05 07:00:00 | Good
 2017-11-05 08:00:00 | Good
 2017-11-05 09:00:00 | Good
 2017-11-05 10:00:00 | Good
 2017-11-05 11:00:00 | Good
 2017-11-05 12:00:00 | Good
 2017-11-05 13:00:00 | Good
 2017-11-05 14:00:00 | Bad
 2017-11-05 15:00:00 | Good
 2017-11-05 16:00:00 | Bad
 2017-11-05 17:00:00 | Good
 2017-11-05 18:00:00 | Bad
 2017-11-05 19:00:00 | Bad
 2017-11-05 20:00:00 | Bad
 2017-11-05 21:00:00 | Good
 2017-11-05 22:00:00 | Good
 2017-11-05 23:00:00 | Good
(24 rows)
```

---

## Tarefa 4 — Corridas por empresa em 15–16 Nov 2017

### Consulta

```sql
SELECT c.company_name,
       COUNT(t.trip_id) AS trips_amount
FROM trips t
JOIN cabs c ON t.cab_id = c.cab_id
WHERE t.start_ts BETWEEN '2017-11-15 00:00:00' AND '2017-11-16 23:59:59'
GROUP BY c.company_name
ORDER BY trips_amount DESC;
```

**Conceito aplicado:** `JOIN` entre `trips` e `cabs` pela chave `cab_id`, com filtro por intervalo de datas e ordenação decrescente por volume.

### Resultado (top 10 de 64 empresas)

```
                 company_name                 | trips_amount 
----------------------------------------------+--------------
 Flash Cab                                    |        19558
 Taxi Affiliation Services                    |        11422
 Medallion Leasin                             |        10367
 Yellow Cab                                   |         9888
 Taxi Affiliation Service Yellow              |         9299
 Chicago Carriage Cab Corp                    |         9181
 City Service                                 |         8448
 Sun Taxi                                     |         7701
 Star North Management LLC                    |         7455
 Blue Ribbon Taxi Association Inc.            |         5953
 [+ 54 empresas adicionais]
(64 rows)
```
