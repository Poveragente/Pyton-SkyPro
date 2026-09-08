import allure
import pytest
from selenium import webdriver

from pages.calc_page import CalsPage


@pytest.fixture
def driver():
    drv = webdriver.Chrome()
    yield drv
    drv.quit()

@allure.severity("blocker")
@allure.title("Тест калькулятора")
@allure.description("Калькулятор медленный")
@allure.feature("Выдача результата зависит от таймера")
def test_cals(driver):
    page = CalsPage(driver, "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

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
