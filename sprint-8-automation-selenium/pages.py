from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from helpers import retrieve_phone_code
import time


class UrbanRoutesPage:
    # POM do Urban Routes para agrupar localizadores e métodos reutilizáveis para os fluxos
    # Localizadores
    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')
    CALL_TAXI_BUTTON_LOCATOR = (By.XPATH,
                                "//button[@type='button' and contains(@class,'round') and text()='Chamar um táxi']")
    COMFORT_PLAN_BUTTON_LOCATOR = (By.XPATH, '//div[contains(text(), "Comfort")]')
    CURRENT_TARIFF = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-title"]')

    PHONE_FIELD_TRIGGER_LOCATOR = (By.XPATH, "//div[@class='np-text']")
    REGISTERED_PHONE = (By.XPATH, '//div[contains(@class, "np-text")]')
    PHONE_INPUT_LOCATOR = (By.ID, 'phone')
    REQUEST_CODE_BUTTON_LOCATOR = (By.XPATH, "//button[text()='Próximo']")
    SMS_CODE_INPUT_LOCATOR = (By.ID, 'code')
    PHONE_CONFIRM_BUTTON_LOCATOR = (By.XPATH, "//button[@type='submit' and text()='Confirmar']")

    ADD_PAYMENT_METHOD = (By.CSS_SELECTOR, '.pp-button.filled')
    ADD_CARD = (By.CSS_SELECTOR, '.pp-plus')
    CARD_NUMBER = (By.ID, 'number')
    CARD_CODE = (By.CSS_SELECTOR, '.card-code-input .card-input')
    ADD_CARD_FINAL = (By.XPATH, "//button[contains(text(),'Adicionar')]")
    CLOSE_BUTTON_CARD = (By.CSS_SELECTOR, '.payment-picker.open .close-button.section-close')
    CONFIRM_CARD = (By.CSS_SELECTOR, '.pp-value-text')
    CURRENT_PAYMENT = (By.XPATH, '//div[contains(@class, "pp-value-text")]')

    COMMENT_INPUT_LOCATOR = (By.ID, 'comment')

    EXTRAS_DROPDOWN_ARROW_LOCATOR = (By.XPATH, "//img[@alt='Arrow']")
    BLANKET_TOGGLE_LOCATOR = (By.XPATH, "//div[contains(text(),'Cobertor e lençóis')]/..//span[@class='slider round']")
    BLANKET_CHECKBOX_LOCATOR = (By.XPATH,
                                "//div[contains(text(),'Cobertor e lençóis')]/..//input[@class='switch-input']")
    ICE_CREAM_COUNTER_PLUS_LOCATOR = (By.XPATH, "//div[@class='counter-plus']")
    ICE_CREAM_COUNTER_VALUE_LOCATOR = (By.XPATH, "//div[@class='counter-value']")
    REQUEST_CAR_BUTTON_LOCATOR = (By.XPATH, "//span[@class='smart-button-main']")
    CAR_SEARCH_INDICATOR_LOCATOR = (By.CLASS_NAME, 'order')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

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

    # Rota
    def set_route(self, address_from, address_to):
        """POM combinado: preenche origem, destino e chama o táxi."""
        self._fill_from(address_from)
        self._fill_to(address_to)
        self._click_call_taxi()

    def _fill_from(self, address_from):
        from_field = self.wait.until(EC.visibility_of_element_located(self.FROM_LOCATOR))
        from_field.send_keys(address_from)

    def _fill_to(self, address_to):
        self.driver.find_element(*self.TO_LOCATOR).send_keys(address_to)

    def _click_call_taxi(self):
        button = self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON_LOCATOR))
        button.click()

    def get_to_value(self):
        return self.driver.find_element(*self.TO_LOCATOR).get_attribute('value')

    # Plano
    def select_comfort_plan(self):
        button = self.wait.until(EC.element_to_be_clickable(self.COMFORT_PLAN_BUTTON_LOCATOR))
        if 'active' not in button.get_attribute('class'):
            button.click()

    # Telefone
    def fill_phone_number(self, phone_number):
        self.wait.until(EC.element_to_be_clickable(self.PHONE_FIELD_TRIGGER_LOCATOR)).click()
        phone_input = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT_LOCATOR))
        phone_input.send_keys(phone_number)
        self.wait.until(EC.element_to_be_clickable(self.REQUEST_CODE_BUTTON_LOCATOR)).click()

        sms_code = retrieve_phone_code(self.driver)

        code_field = self.wait.until(EC.visibility_of_element_located(self.SMS_CODE_INPUT_LOCATOR))
        code_field.send_keys(sms_code)
        self.wait.until(EC.element_to_be_clickable(self.PHONE_CONFIRM_BUTTON_LOCATOR)).click()
        self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))

    def enter_sms_code(self, code):
        code_field = self.wait.until(EC.visibility_of_element_located(self.SMS_CODE_INPUT_LOCATOR))
        code_field.send_keys(code)
        self.wait.until(EC.element_to_be_clickable(self.PHONE_CONFIRM_BUTTON_LOCATOR)).click()


    #Cartão
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

    # Comentário
    def set_driver_comment(self, message):
        field = self.wait.until(EC.visibility_of_element_located(self.COMMENT_INPUT_LOCATOR))
        field.send_keys(message)

    # Extras
    def _open_extras_dropdown(self):
        try:
            WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(self.BLANKET_TOGGLE_LOCATOR))
            return  # já está aberto, não faz nada
        except TimeoutException:
            pass
        self._safe_click(self.EXTRAS_DROPDOWN_ARROW_LOCATOR)
        self.wait.until(EC.visibility_of_element_located(self.BLANKET_TOGGLE_LOCATOR))

    def order_blanket_and_handkerchiefs(self):
        self._open_extras_dropdown()
        self.wait.until(EC.element_to_be_clickable(self.BLANKET_TOGGLE_LOCATOR)).click()

    def is_blanket_ordered(self):
        checkbox = self.driver.find_element(*self.BLANKET_CHECKBOX_LOCATOR)
        return checkbox.is_selected()

    def order_ice_creams(self, count=2):
        self._open_extras_dropdown()
        for _ in range(count):
            self._safe_click(self.ICE_CREAM_COUNTER_PLUS_LOCATOR)

    def get_ice_cream_count(self):
        value = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_COUNTER_VALUE_LOCATOR))
        return int(value.text)

    # Buscar carro
    def request_taxi(self):
        self._safe_click(self.REQUEST_CAR_BUTTON_LOCATOR)

    def is_car_search_modal_visible(self):
        self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_INDICATOR_LOCATOR))
        return True

    def get_selected_tariff(self):
        return self.wait.until(EC.visibility_of_element_located(self.CURRENT_TARIFF)).text

    def get_phone_number(self):
        return self.wait.until(EC.visibility_of_element_located(self.REGISTERED_PHONE)).text

    def get_payment_method(self):
        return self.wait.until(EC.visibility_of_element_located(self.CURRENT_PAYMENT)).text

    def get_driver_comment(self):
        return self.wait.until(EC.visibility_of_element_located(self.COMMENT_INPUT_LOCATOR)).get_attribute('value')