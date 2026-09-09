# 🧪 Sprint 7 —  Urban Routes: Introdução à Automação de Testes

## 📋 Sobre o projeto

Este é o primeiro de dois projetos de automação (Sprint 7 + Sprint 8) que testam a aplicação **Urban Routes**, anteriormente testada manualmente nos sprints anteriores.

Neste projeto foi estabelecida a base da suite de automação: separação de dados de teste, código auxiliar (helper) e a estrutura da classe de testes com Pytest, pronta para receber o código Selenium no Sprint 8.

---

## 🗂️ Estrutura de ficheiros

| Ficheiro       | Descrição                                                                                     |
| -------------- | ---------------------------------------------------------------------------------------------- |
| `helpers.py`   | Código auxiliar fornecido (não alterado): recuperação do código de confirmação do telefone e verificação de disponibilidade do servidor Urban Routes |
| `data.py`      | Constantes com os dados de teste (URL, morada de origem/destino, telefone, cartão, mensagem para o motorista) |
| `main.py`      | Classe `TestUrbanRoutes` com verificação do servidor (`setup_class`) e 8 funções de teste vazias, preparadas para o Sprint 8 |

---

## ✅ Tarefas realizadas

- [x] Criação de `helpers.py` com o código auxiliar fornecido (inalterado)
- [x] Adição das constantes de dados de teste em `data.py`
- [x] Criação da classe `TestUrbanRoutes` em `main.py` com 8 métodos de teste (`test_set_route`, `test_select_plan`, `test_fill_phone_number`, `test_fill_card`, `test_comment_for_driver`, `test_order_blanket_and_handkerchiefs`, `test_order_2_ice_creams`, `test_car_search_model_appears`)
- [x] Implementação de `setup_class` para verificar se o servidor Urban Routes está acessível, usando `is_url_reachable` de `helpers.py`
- [x] Preparação do ciclo `for` dentro de `test_order_2_ice_creams` (2 iterações), pronto para receber a lógica do Selenium no próximo sprint

---

## 🛠️ Ferramentas utilizadas

- **Linguagem**: Python 3
- **Test framework**: Pytest
- **IDE**: PyCharm
- **Controlo de versões**: Git / GitHub
- **Ambiente**: ambiente virtual (`venv`) dedicado ao projeto

---

## ➡️ Próximos passos (Sprint 8)

No Sprint 8, cada função de teste vai receber a lógica Selenium correspondente (localização de elementos, ações no browser, asserts), substituindo os comentários `# Adicionar em S8`.
