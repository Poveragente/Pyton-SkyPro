import allure
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

    def __init__(self, driver, url, str) -> None:
        """Инициализирует страницу калькулятора.
        Args:
            driver: Экземпляр WebDriver для управления браузером.
            url: URL страницы калькулятора.
        """
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(self.driver, 60)

    @allure.step("Метод открытия калькулятора")
    def open_cals(self) -> None:
        self.driver.get(self.url)
    """
            Метод выставление задержки для медленного калькулятора 
    """
    @allure.step("Метод выставления задержки")
    def delay_input(self, value="12") -> None:
        """Устанавливает значение задержки для медленного калькулятора.
         Args:
             value: Значение задержки в секундах. По умолчанию — 15.
         """
        with (allure.step(
                "Находим поле в которое записывается"
                "значение в секундах, проверяем что оно кликабельно"
        )):
            delay_input = self.wait.until
            (EC.element_to_be_clickable(self.DELAY_INPUT))
        with allure.step("Очищаем поле"):
            delay_input.clear()
        with allure.step("выставляем значение задержки"):
            delay_input.send_keys(15)

    @allure.step("Метод прокликивания ")
    def click_btn(self, locator: tuple[By, str]) -> None:
        """Выполняет клик по элементу, найденному по локатору.
        Сначала ожидает, пока элемент станет кликабельным.
        Args:
            locator: Кортеж (тип локатора, значение), например (By.ID, "btn").
        btn = self.wait.until(EC.element_to_be_clickable(locator))
        btn.click()
    """

    @allure.step("Метод складывающий 2 числа")
    def sloshenie(self) -> None:
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

    @allure.step("Возвращение результата "
                 "работы калькулятора")
    def get_result(self) -> str:
        """
        Ожидает появления результата «15»
        на экране и возвращает текст результата.
        Returns:
            Текст, отображаемый на экране калькулятора
            (результат операции).
        """
        with allure.step("Выставляем таймер ожидания"):
            wait = WebDriverWait(self.driver, 60)
        with allure.step("Ожидание текста "
                         "с нужным результатом "):
            wait.until(EC.text_to_be_present_in_element
                       ((By.CLASS_NAME, "screen"), "15"))

        result_element = (self.wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "screen"))))
        return result_element.text
