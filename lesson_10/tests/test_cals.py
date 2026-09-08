import allure
import pytest
from selenium import webdriver

from pages.calc_page import CalsPage


@pytest.fixture
def driver() -> webdriver.Chrome:
    """Создаёт экземпляр Chrome WebDriver
    и корректно завершает его работу после теста.
        Yields:
            webdriver.Chrome: Инициализированный драйвер браузера.
        """
    drv = webdriver.Chrome()
    yield drv
    drv.quit()


@allure.severity("blocker")
@allure.title("Тест калькулятора")
@allure.description("Калькулятор медленный")
@allure.feature("Выдача результата зависит от таймера")
def test_cals(driver) -> None:
    """
    Проверяет корректность работы медленного калькулятора
    с выставленной задержкой.
        Сценарий:
          1. Открыть страницу калькулятора.
          2. Установить задержку 45 секунд.
          3. Выполнить операцию 7 + 8.
          4. Убедиться, что результат равен "15".
        Args:
            driver: Экземпляр Chrome WebDriver, предоставляемый фикстурой.
        """
    page = CalsPage(driver, "https://bonigarcia.dev/selenium"
                            "-webdriver-java/slow-calculator.html")

    with allure.step("открываем страницу калькулятора"):
        page.open_cals()
    with allure.step("Выставляем задержку [page.delay_input]"):
        page.delay_input(45)
    with allure.step("Выполняем сложение"):
        page.sloshenie()
    with allure.step("Сохраняем результат"):
        result = page.get_result()
    with allure.step("проверяем что результат равен [result]"):
        assert result == "15"
