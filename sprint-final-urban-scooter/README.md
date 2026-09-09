# Sprint Final — Urban Scooter: Testes Web, Mobile e Backend/API

Projeto final do bootcamp de QA (TripleTen), focado em testar de ponta a ponta a aplicação **Urban Scooter**: a interface web, a aplicação mobile e o backend/API. O objetivo foi analisar requisitos, desenhar casos de teste, executá-los, reportar bugs no Jira e documentar os resultados.

## Índice

- [Objetivo](#objetivo)
- [Escopo do projeto](#escopo-do-projeto)
- [Técnicas de teste utilizadas](#técnicas-de-teste-utilizadas)
- [Ferramentas](#ferramentas)
- [Tarefa 1 — Aplicação Web](#tarefa-1--aplicação-web)
- [Tarefa 2 — Aplicação Mobile](#tarefa-2--aplicação-mobile)
- [Tarefa 3 — Backend / API](#tarefa-3--backendapi)
- [Bugs reportados](#bugs-reportados)
- [Estrutura do repositório](#estrutura-do-repositório)

## Objetivo

Validar o comportamento da aplicação Urban Scooter (web, mobile e backend) face aos requisitos fornecidos, identificando desvios de comportamento, ambiguidades nos requisitos e reportando defeitos de forma rastreável no Jira.

## Escopo do projeto

| Tarefa | Componente | O que foi testado |
|---|---|---|
| 1 | Aplicação Web | Formulário "Para quem é a scooter" (Nome, Sobrenome, Endereço, Estação de metro, Telefone) + fluxo E2E, em Chrome e Opera (1280x720) |
| 2 | Aplicação Mobile | Notificações, deteção de falha de rede, orientação de ecrã, login (username/senha) — testado em emulador Android via Android Studio |
| 3 | Backend / API | Endpoints de criação e exclusão de entregadores (Postman), com verificação cruzada na base de dados PostgreSQL |

## Técnicas de teste utilizadas

- **Particionamento em classes de equivalência** — para identificar conjuntos de valores válidos e inválidos por campo.
- **Análise de valores-limite (Boundary Value Analysis)** — testar os limites mínimo/máximo de cada campo (ex.: 1 vs. 2 caracteres, 15 vs. 16 caracteres).
- **Teste de caixa-preta funcional** — validação do comportamento face aos requisitos, sem conhecimento da implementação interna.
- **Testes E2E (ponta a ponta)** — fluxo completo de preenchimento e submissão do formulário de pedido, incluindo combinações de campos válidos/inválidos.
- **Teste exploratório** — investigação de comportamentos não especificados nos requisitos (ex.: tecla Enter no campo de estação, edição manual de um campo pré-preenchido, aceitação de alfabetos não latinos).
- **Testes cross-browser** — execução dos mesmos casos de teste em Chrome e Opera para validar consistência entre navegadores.
- **Teste de API (Postman)** — validação de endpoints do backend com diferentes payloads (campos em falta, valores fora dos limites, tipos de dados inválidos).
- **Validação cruzada com a base de dados (PostgreSQL)** — confirmação do estado dos dados diretamente na base de dados após operações via API.

## Ferramentas

- **Jira** — registo e acompanhamento de bugs
- **Google Sheets** — desenho e documentação dos casos de teste e resultados
- **Figma** — validação de layout e design
- **Android Studio (emulador)** — testes da aplicação mobile
- **Postman** — testes de API
- **psql (PostgreSQL)** — verificação da base de dados
- **Chrome / Opera** — testes cross-browser da aplicação web

## Tarefa 1 — Aplicação Web

Foram desenhados e executados **73 casos de teste** para o formulário "Para quem é a scooter" (primeiro estágio do fluxo "Fazer pedido"), cobrindo os campos Nome, Sobrenome, Endereço, Estação de metro e Telefone, além de 9 cenários E2E de submissão do formulário (combinações de campos válidos/inválidos e persistência de dados ao navegar entre estágios).

Todos os casos de teste incluem: pré-condições, passos, classe de equivalência / valor-limite, dados de teste, resultado esperado e resultado obtido em Chrome e Opera (1280x720).

**Resultados por campo:**

| Campo | Casos de teste | Bugs encontrados |
|---|---|---|
| Nome | TC-01 a TC-17 | Não aceita acentuação (deveria aceitar, por não haver alfabeto especificado nos requisitos) |
| Sobrenome | TC-18 a TC-34 | Aceita 16 caracteres (fora do limite máximo); não aceita acentuação |
| Endereço | TC-35 a TC-48 | Aceita 50 caracteres (fora do limite máximo); aceita campo vazio |
| Estação de metro | TC-48 a TC-54 | Erro de aplicação ("Unexpected Application Error") ao pressionar Enter; valor não pode ser editado/apagado manualmente após seleção |
| Telefone | TC-55 a TC-64 | Aceita 10 caracteres (abaixo do mínimo); aceita 13 caracteres (acima do máximo); aceita ausência do símbolo "+" |
| E2E | TC-65 a TC-73 | Sem bugs — todos aprovados |

## Tarefa 2 — Aplicação Mobile

**Nota importante:** a execução desta tarefa foi bloqueada por uma instabilidade conhecida da aplicação mobile. Foi possível confirmar, via teste de API, que o entregador foi criado com sucesso — mas não foi possível efetuar login na app, o que impediu a execução dos casos de teste desenhados (T2-01 a T2-20).

Os casos de teste foram na mesma desenhados, cobrindo:
- **Notificações** — receção da notificação exatamente 2h antes do prazo, conteúdo da notificação, correspondência ao pedido correto, navegação ao tocar na notificação
- **Falha de conexão à internet** — exibição, persistência e fecho do pop-up "Sem acesso à internet"
- **Orientação do ecrã** — funcionamento em retrato e restrição a paisagem
- **Login** — limites de caracteres do username (2–10) e da senha (exatamente 4 dígitos numéricos), rejeição de valores inválidos e mensagem de erro para credenciais incorretas

Estado: todos os 20 casos de teste ficaram como **"Não executado"** devido à instabilidade da app, sem bugs reportados nesta tarefa.

## Tarefa 3 — Backend / API

Testado o backend do Urban Scooter com Postman (33 casos de teste), com foco nos endpoints de **criação** (`POST /api/v1/courier`) e **exclusão** (`DELETE /api/v1/courier/{id}`) de entregadores. Os resultados foram cruzados com a base de dados PostgreSQL (`scooter_rent`) sempre que possível.

Esta foi a tarefa com mais bugs encontrados: a API aceitou, de forma consistente, valores que deveriam ser rejeitados nos campos `login`, `firstName` e `password` (números, caracteres especiais, acentuação, espaços e comprimentos fora dos limites definidos nos requisitos), e devolveu um erro 500 (em vez de 400) ao receber um ID inválido no endpoint de exclusão.

## Bugs reportados

Todos os bugs foram registados no Jira, com o resultado esperado, o resultado obtido e passos para reprodução.

| ID | Tarefa | Descrição resumida |
|---|---|---|
| [PFS9-1](https://ricardoneto027.atlassian.net/browse/PFS9-1) | Web | Estação de metro não pode ser editada/apagada manualmente após seleção |
| [PFS9-2](https://ricardoneto027.atlassian.net/browse/PFS9-2) | Web | Campo "Telefone" aceita 10 caracteres, abaixo do limite mínimo |
| [PFS9-3](https://ricardoneto027.atlassian.net/browse/PFS9-3) | Web | Campo "Endereço" aceita valor vazio |
| [PFS9-4](https://ricardoneto027.atlassian.net/browse/PFS9-4) | Web | Erro de aplicação ao pressionar Enter no campo Estação |
| [PFS9-5](https://ricardoneto027.atlassian.net/browse/PFS9-5) | Web | Campo "Telefone" aceita 13 caracteres, acima do limite máximo |
| [PFS9-6](https://ricardoneto027.atlassian.net/browse/PFS9-6) | API | Exclusão com ID em formato inválido devolve 500 Internal Server Error em vez de 400 |
| [PFS9-7](https://ricardoneto027.atlassian.net/browse/PFS9-7) | Web | Campo "Sobrenome" não aceita caracteres acentuados |
| [PFS9-8](https://ricardoneto027.atlassian.net/browse/PFS9-8) | Web | Campo "Endereço" aceita 50 caracteres, acima do limite máximo |
| [PFS9-9](https://ricardoneto027.atlassian.net/browse/PFS9-9) | Web | Campo "Nome" não aceita caracteres acentuados |
| [PFS9-10](https://ricardoneto027.atlassian.net/browse/PFS9-10) | Web | Campo "Sobrenome" aceita 16 caracteres, acima do limite máximo |
| [PFS9-11](https://ricardoneto027.atlassian.net/browse/PFS9-11) | API | Campo `password` aceita letras, caracteres especiais e comprimentos fora de 4 dígitos |
| [PFS9-12](https://ricardoneto027.atlassian.net/browse/PFS9-12) | API | Comportamento inesperado ao consultar pedidos de um entregador com pedidos associados |
| [PFS9-13](https://ricardoneto027.atlassian.net/browse/PFS9-13) | API | Campo `login` aceita mais de 10 caracteres |
| [PFS9-14](https://ricardoneto027.atlassian.net/browse/PFS9-14) | API | Campo `firstName` aceita números, caracteres especiais, alfabetos não latinos e comprimentos fora dos limites |
| [PFS9-15](https://ricardoneto027.atlassian.net/browse/PFS9-15) | Web | Campo "Telefone" aceita número sem o símbolo "+" obrigatório |
| [PFS9-16](https://ricardoneto027.atlassian.net/browse/PFS9-16) | API | Campo `login` aceita números |
| [PFS9-17](https://ricardoneto027.atlassian.net/browse/PFS9-17) | API | Campo `login` aceita espaços |
| [PFS9-18](https://ricardoneto027.atlassian.net/browse/PFS9-18) | API | Campo `login` aceita valores abaixo do limite mínimo |
| [PFS9-19](https://ricardoneto027.atlassian.net/browse/PFS9-19) | API | Campo `login` aceita caracteres especiais |
| [PFS9-20](https://ricardoneto027.atlassian.net/browse/PFS9-20) | API | Campo `login` aceita caracteres acentuados |

## Estrutura do repositório

```
sprint-final-urban-scooter/
├── README.md
└── Ricardo_Peres_QA30_Projeto_Final.xlsx   # Casos de teste, resultados e links de bugs
```

---
*Projeto final do bootcamp de QA Engineer — TripleTen*
