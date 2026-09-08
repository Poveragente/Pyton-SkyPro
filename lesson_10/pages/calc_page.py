from pydoc import text

import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CalsPage:
    DELAY_INPUT = (By.ID, "delay")
    CHISLO_ONE = (By.XPATH, "//span[contains(text(), '7')]")
    OPERATOR_PLUS = (By.XPATH, "//span[contains(text(), '+')]")
    CHISLO_TWO = (By.XPATH, "//span[contains(text(), '8')]")
    OPERATOR_RAVNO = (By.XPATH, "//span[contains(text(), '=')]")
    SCREEN_RES = (By.CLASS_NAME, "screen")

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(self.driver, 60)

    @allure.step("Метод открытия калькулятора")
    def open_cals(self):
        self.driver.get(self.url)
    """
    Метод выставление задержки для медленного калькулятора 
    """

    @allure.step("Метод выставления задержки")
    def delay_input(self, value="12"):
        with allure.step("Находим поле в которое записывается значение в секундах, проверяем что оно кликабельно "):
            delay_input = self.wait.until(EC.element_to_be_clickable(self.DELAY_INPUT))
        with allure.step("Очищаем поле"):
            delay_input.clear()
        with allure.step("выставляем значение задержки"):
            delay_input.send_keys(15)

    @allure.step("Метод прокликивания ")
    def click_btn(self, locator):
        btn = self.wait.until(EC.element_to_be_clickable(locator))
        btn.click()
    """
        Метод прокликивающий кнопки "7" "+" "8" "="
    """

    @allure.step("Метод складывающий 2 числа")
    def sloshenie(self):
        with allure.step("Клик на первое число"):
            self.click_btn(self.CHISLO_ONE)
        with allure.step("Клик на оператор + "):
            self.click_btn(self.OPERATOR_PLUS)
        with allure.step("Клик на второе число"):
            self.click_btn(self.CHISLO_TWO)
        with allure.step("Клик на оператор = "):
            self.click_btn(self.OPERATOR_RAVNO)
    """
        Метод возвращающий результат работы калькулятора
    """
    @allure.step("Возвращение результата работы калькулятора")
    def get_result(self):
        with allure.step("Выставляем таймер ожидания"):
            wait = WebDriverWait(self.driver, 60)
        with allure.step("Ожидание текста с нужным результатом "):
            wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15"))

        result_element = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "screen")))
        return result_element.text

