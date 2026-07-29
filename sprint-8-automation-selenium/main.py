import data
import helpers
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from pages import UrbanRoutesPage

class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.get(data.URBAN_ROUTES_URL)
        cls.page = UrbanRoutesPage(cls.driver)
        #cls.driver.maximize_window()
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não é possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

    def test_set_route(self):
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.page.get_to_value() == data.ADDRESS_TO

    def test_select_plan(self):
        self.page.select_comfort_plan()
        assert self.page.get_selected_tariff() == "Comfort"

    def test_fill_phone_number(self):
        self.page.fill_phone_number(data.PHONE_NUMBER)
        assert self.page.get_phone_number() == data.PHONE_NUMBER

    def test_fill_card(self):
        self.page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.page.get_payment_method() == "Cartão"

    def test_comment_for_driver(self):
        self.page.set_driver_comment(data.MESSAGE_FOR_DRIVER)
        assert self.page.get_driver_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self.page.order_blanket_and_handkerchiefs()
        assert self.page.is_blanket_ordered()

    def test_order_2_ice_creams(self):
        self.page.order_ice_creams(2)
        assert self.page.get_ice_cream_count() == 2

    def test_car_search_model_appears(self):
        self.page.request_taxi()
        assert self.page.is_car_search_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()