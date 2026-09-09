# Sprint 8 — Urban Routes: Automação de Testes com Python + Selenium

Projeto do **Sprint 8** do bootcamp de QA/Software Testing da **TripleTen**, com automação end-to-end do fluxo de pedido de viagem da aplicação fictícia **Urban Routes**, usando **Python**, **Selenium WebDriver** e **pytest**, seguindo o padrão de design **Page Object Model (POM)**.

Estado final: ✅ **8/8 testes a passar**.

---

## 📋 Índice

- [Objetivo do projeto](#objetivo-do-projeto)
- [Stack técnica](#stack-técnica)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Arquitetura: Page Object Model](#arquitetura-page-object-model)
- [Fluxo testado](#fluxo-testado)
- [Como correr os testes](#como-correr-os-testes)
- [Processo de debugging — os 5 bugs reais](#processo-de-debugging--os-5-bugs-reais)
- [Uso de IA (Claude) no processo](#uso-de-ia-claude-no-processo)
- [Lições aprendidas](#lições-aprendidas)
- [Próximos passos](#próximos-passos)

---

## Objetivo do projeto

Construir uma suite de testes automatizados que simula o percurso completo de um utilizador na aplicação Urban Routes:

1. Definir o endereço;
2. Selecionar o plano Comfort (dica: não se esqueça de fazer uma condição if se esta tarifa for selecionada ou não para evitar cliques desnecessários que levam a falhas nos testes);
3. Preencher o número de telefone (dica: não se esqueça de usar o método retrieve_phone_code() do arquivo helpers.py para recuperar o código SMS);
4. Adicionar um cartão de crédito (dica: o botão "Adicionar" pode não ficar clicável até que o campo CVV do cartão no modal "Adicione cartão" id="code" class="card-input" perca o foco. Para alterar o foco, você pode simular o usuário pressionando a aba ou clicando em outro lugar na tela);
5. Escrever um comentário para o motorista;
6. Pedir um cobertor e lenços (dica: há dois seletores que você deve conhecer aqui. Um seletor para clicar e outro para executar assert para verificar se o estado mudou);
7. Pedir 2 sorvetes;
8. Pedir um táxi com a tarifa "Comfort". A janela modal de busca de carros deve aparecer (dica: ao fazer o pedido, não se esqueça de adicionar uma mensagem para o motorista).

Cada etapa corresponde a um teste `pytest` independente, mas que corre sobre a **mesma sessão do browser** (sem recarregar a página entre testes), simulando um fluxo real e contínuo de utilizador.

## Stack técnica

| Ferramenta | Função |
|---|---|
| Python 3.14 | Linguagem base |
| Selenium WebDriver | Automação do browser |
| pytest | Framework de testes e execução |
| PyCharm | IDE |
| ChromeDriver | Driver do Chrome |
| macOS (Apple Silicon) | Ambiente de desenvolvimento |

## Estrutura do projeto

```
QA-Brazil_Python_Automation/
├── main.py          # Suite de testes (classe TestUrbanRoutes)
├── pages.py         # Page Object (classe UrbanRoutesPage)
├── data.py           # Dados de teste (endereços, telefone, cartão, mensagens)
├── helpers.py        # Funções auxiliares (ex: obter código SMS, verificar URL)
└── README.md
```

## Arquitetura: Page Object Model

O projeto segue o padrão **POM**, isolando toda a lógica de interação com a página numa única classe (`UrbanRoutesPage`), separada da lógica de teste (`TestUrbanRoutes`). Isto traz três vantagens práticas que se confirmaram durante o desenvolvimento:

- **Manutenibilidade**: quando um seletor CSS/XPath muda ou está errado, só é preciso corrigir num sítio (`pages.py`), não em cada teste.
- **Legibilidade**: os testes em `main.py` lêem-se quase como frases (`self.page.fill_card(...)`, `self.page.request_taxi()`), sem detalhes de implementação.
- **Reutilização**: métodos como `_safe_click()` são partilhados por várias ações (extras, sorvetes, pedido de táxi).

Exemplo da estrutura de um método do Page Object:

```python
def fill_card(self, card_number, card_code):
    self.wait.until(EC.element_to_be_clickable(self.ADD_PAYMENT_METHOD)).click()
    self.wait.until(EC.element_to_be_clickable(self.ADD_CARD)).click()

    self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER)).send_keys(card_number)
    code_field = self.wait.until(EC.visibility_of_element_located(self.CARD_CODE))
    code_field.click()
    code_field.send_keys(card_code)
    code_field.send_keys(Keys.TAB)
    self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_FINAL)).click()
    self.wait.until(EC.element_to_be_clickable(self.CLOSE_BUTTON_CARD)).click()
```

Note que todas as esperas foram substituídas por condições explícitas do Selenium (`WebDriverWait` + `expected_conditions`), eliminando os antigos `time.sleep()` fixos — uma prática mais robusta e mais rápida, porque a espera termina assim que a condição é satisfeita, em vez de aguardar sempre um tempo fixo.

### Padrão "Safe Click" (retry pattern)

Para lidar com instabilidade de UI comum em aplicações web reais (elementos que ainda estão a animar/estabilizar quando o Selenium tenta clicar), foi implementado um método reutilizável de **retry** com tratamento de exceção:

```python
def _safe_click(self, locator, timeout=10):
    """Tenta clicar num elemento, repetindo se o clique for intercetado."""
    end_time = time.time() + timeout
    last_exception = None
    while time.time() < end_time:
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return
        except ElementClickInterceptedException as e:
            last_exception = e
            time.sleep(0.5)
    raise TimeoutException(f"Elemento {locator} continua bloqueado após {timeout}s") from last_exception
```

Este padrão é standard em automação profissional (não usa JavaScript nem contorna o Selenium — apenas combina `WebDriverWait`, `expected_conditions` e `try/except` de forma mais robusta).

## Fluxo testado

| Teste | O que valida |
|---|---|
| `test_set_route` | Origem e destino são preenchidos e mantidos corretamente |
| `test_select_plan` | Plano "Comfort" fica selecionado (classe `active`) |
| `test_fill_phone_number` | Número de telefone é confirmado após fluxo de SMS |
| `test_fill_card` | Cartão é adicionado e o método de pagamento passa a "Cartão" |
| `test_comment_for_driver` | Comentário ao motorista é guardado no campo |
| `test_order_blanket_and_handkerchiefs` | Toggle de cobertor/lençóis fica ativo |
| `test_order_2_ice_creams` | Contador de sorvetes chega a 2 |
| `test_car_search_model_appears` | Modal de busca de carro aparece ao pedir o táxi |

## Como correr os testes

```bash
# a partir da raiz do projeto, com o venv ativo
pytest main.py -v
```

Pré-requisitos: ChromeDriver compatível com a versão do Chrome instalada, e o servidor Urban Routes acessível (verificado automaticamente no `setup_class` via `helpers.is_url_reachable`).

---

## Processo de debugging — os 5 bugs reais

Esta secção documenta o processo real de resolução de falhas, porque foi a parte mais valiosa do sprint em termos de aprendizagem prática de QA. Cada bug tinha uma causa raiz diferente, e vários deles pareciam, à primeira vista, o mesmo problema.

### 1. `element click intercepted` no botão de fechar do cartão (falso diagnóstico inicial)

**Sintoma:** depois de preencher os dados do cartão, o clique no botão "X" para fechar a modal de "Método de pagamento" não tinha efeito. O erro do Selenium apontava para "elemento não clicável nesse ponto", com outro elemento (`div.section.active`) a "roubar" o clique.

**Hipóteses testadas e descartadas, por ordem:**
- ❌ Tentar `send_keys(Keys.ESCAPE)` em vez de `.click()` — não funcionou, porque o botão não tinha listener de teclado, só de clique.
- ❌ Retry loop / espera adicional — não resolveu, porque o problema não era de timing.
- ❌ `transform: scale(2)` no CSS a desalinhar o bounding box — hipótese razoável mas descartada depois de inspecionar o DOM diretamente.

**Causa raiz real:** o seletor CSS estava **sintaticamente incorreto**:

```python
# Errado — "payment-picker-open" como classe única (não existe)
CLOSE_BUTTON_CARD = (By.CSS_SELECTOR, '.payment-picker-open .close-button.section-close')

# Correto — duas classes distintas no mesmo elemento (payment-picker E open)
CLOSE_BUTTON_CARD = (By.CSS_SELECTOR, '.payment-picker.open .close-button.section-close')
```

**Como foi confirmado:** ao correr `document.querySelector('.close-button.section-close').getBoundingClientRect()` na consola do DevTools, o resultado devolveu um `DOMRect` todo a zero (`width: 0, height: 0, x: 0, y: 0`) — sinal de que o seletor original não apontava para o elemento visível, mas provavelmente para um elemento inexistente ou duplicado escondido no DOM.

**Efeito cascata:** como a modal nunca fechava de verdade, os 3 testes seguintes (cobertor, sorvetes, pedido de táxi) falhavam todos com o mesmo erro (`overlay`/`section active` a bloquear cliques) — um único bug de CSS a propagar-se por toda a suite.

### 2. `AttributeError: 'UrbanRoutesPage' object has no attribute '_safe_click'`

**Sintoma:** mesmo depois de adicionar o método `_safe_click`, o erro persistia.

**Causa raiz:** erro de indentação — o método tinha ficado definido **dentro** do `__init__`, tornando-se uma função local que desaparece após a execução do construtor, em vez de um método da classe:

```python
# Errado
def __init__(self, driver):
    self.driver = driver
    self.wait = WebDriverWait(driver, 10)

    def _safe_click(self, locator, timeout=10):   # indentado a mais → função local, não método
        ...

# Correto
def __init__(self, driver):
    self.driver = driver
    self.wait = WebDriverWait(driver, 10)

def _safe_click(self, locator, timeout=10):        # mesmo nível de indentação dos outros métodos
    ...
```

**Lição prática:** em Python, a indentação define a estrutura — um erro de um único nível de indentação muda completamente o comportamento do código, sem gerar erro de sintaxe.

### 3. Comparação com ficheiro de outra estudante ("porque é que o dela funciona?")

Durante o processo, foi feita uma comparação com o `pages.py`/`main.py` de uma colega aprovada no bootcamp. A análise revelou que os métodos chamados no `main.py` dela (`switch_comforton`, `add_cartao`, `comentario`) **não correspondiam** aos nomes definidos no `pages.py` dela (`switch_cobertor`, `click_add_cartao`, `add_comentario`) — ou seja, aquela combinação exata de ficheiros nunca teria corrido sem erro. Conclusão: os ficheiros partilhados eram de versões diferentes e não podiam ser usados como prova de que uma abordagem específica "funcionava".

**Lição prática:** copiar código de terceiros sem validar se as peças realmente encaixam entre si pode gerar falsas pistas de debugging — é preciso testar, não assumir.

### 4. Dropdown de extras a abrir/fechar de forma imprevisível

**Sintoma:** o dropdown "Requisitos do pedido" parecia abrir e fechar sozinho de forma aleatória.

**Causa raiz:** a seta de abertura do dropdown é um **acordeão/toggle** — cada clique alterna entre aberto e fechado. Como os testes partilham a mesma sessão do browser (sem recarregar a página), se o dropdown já estava aberto de um teste anterior, um novo clique fechava-o em vez de o abrir. A interferência de cliques manuais do utilizador ao mesmo tempo que o Selenium também tentava clicar agravou a confusão inicial (dois "atores" a alternar o mesmo estado).

**Correção:** tornar o método idempotente — verificar primeiro se o dropdown já está aberto antes de decidir clicar:

```python
def _open_extras_dropdown(self):
    try:
        WebDriverWait(self.driver, 2).until(
            EC.visibility_of_element_located(self.BLANKET_TOGGLE_LOCATOR)
        )
        return  # já está aberto, não faz nada
    except TimeoutException:
        pass
    self._safe_click(self.EXTRAS_DROPDOWN_ARROW_LOCATOR)
    self.wait.until(EC.visibility_of_element_located(self.BLANKET_TOGGLE_LOCATOR))
```

**Lição prática:** ao automatizar toggles/acordeões, nunca assumir o estado inicial — verificar sempre o estado atual antes de agir, especialmente em suites que partilham sessão de browser entre testes.

### 5. `order_ice_creams` a falhar por dependência não explícita

**Sintoma:** o método tentava clicar diretamente no contador de sorvetes, sem garantir que o dropdown de extras (onde o contador vive) estava aberto.

**Correção:** chamar explicitamente `_open_extras_dropdown()` no início do método, tal como já acontecia em `order_blanket_and_handkerchiefs`.

---

## Uso de IA (Claude, ChatGPT, Gemini) no processo

Este projeto foi desenvolvido com apoio do **Claude (Anthropic)**, **ChatGPT (OpenAI)** e **Gemini (Google)** como pares de debugging, seguindo um processo iterativo e disciplinado — não de "copiar-colar soluções", mas de diagnóstico dirigido por evidência:

1. **Partilha do erro completo** (stack trace do pytest) a cada iteração, em vez de descrições vagas do problema.
2. **Rejeição ativa de soluções que não respeitavam o âmbito do curso** — quando uma sugestão envolveu `execute_script` (JavaScript), foi recusada por não fazer parte do currículo da TripleTen, e foi pedida uma alternativa 100% Selenium/Python.
3. **Verificação empírica antes de aceitar hipóteses** — em vez de aplicar cegamente cada sugestão, foram usadas ferramentas do DevTools (`getBoundingClientRect()`, `querySelectorAll().length`, inspeção do HTML real) para confirmar ou refutar cada teoria antes de mexer no código.
4. **Recolha de evidência sem interferência manual** — quando o comportamento parecia inconsistente, foi usado um método de diagnóstico (`debug_dump`, com `save_screenshot` e `page_source`) para capturar o estado real da aplicação no momento exato, eliminando a variável de interação humana simultânea.
5. **Questionamento de fontes externas** — ao receber código de uma colega como referência, a IA foi usada para validar se aquele código realmente era consistente internamente antes de o tratar como prova de que uma abordagem funcionava.

Esta abordagem — descrever o erro exato, testar hipóteses com evidência real do DOM, e recusar atalhos fora do currículo — é também uma boa prática a levar para o dia a dia profissional de QA: a IA acelera o diagnóstico, mas a validação final é sempre feita com dados reais da aplicação.

## Lições aprendidas

- Um `element click intercepted` pode ter várias causas diferentes (timing, CSS `transform`, seletor incorreto, sobreposição de elementos) — a única forma fiável de distinguir é inspecionar o DOM diretamente, não assumir.
- Erros de indentação em Python não geram exceções de sintaxe, mas mudam silenciosamente o comportamento do programa — merece atenção redobrada ao copiar/colar código para dentro de classes.
- Testes que partilham sessão de browser (sem recarregar a página) exigem métodos **idempotentes**, especialmente para elementos do tipo toggle/acordeão.
- Comparar com código de terceiros só é útil se se confirmar primeiro que esse código é internamente consistente.
- O padrão POM comprovou o seu valor prático: a maioria das correções deste sprint foi feita num único ficheiro (`pages.py`), sem tocar nos testes em si.

## Próximos passos

Conforme o roteiro de estudo pós-bootcamp:
- ISTQB Foundation Level
- Python avançado
- PostgreSQL Avançado
- GitHub Actions / GitLab CI/CD
- JMeter via BlazeMeter University
- Katalon Academy

---

*Projeto desenvolvido no âmbito do bootcamp de QA/Software Testing da TripleTen (Fevereiro–Agosto 2026).*
