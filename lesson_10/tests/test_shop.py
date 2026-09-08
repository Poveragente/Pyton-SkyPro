import pytest
import allure
from selenium import webdriver
from pages.shop_page import ShopPage


@pytest.fixture
def driver():
    drv = webdriver.Firefox()
    yield drv
    drv.quit()

@allure.title("Онлайн покупка")
@allure.description(" шмотье ")
@allure.epic("интернет магазин")
@allure.severity("blocker")
@allure.feature("Создание заказа")
def test_shop_flow(driver):
    with allure.step("определяем драйвер "):
        page = ShopPage(driver, "https://www.saucedemo.com/")
    with allure.step("открываем страницу авторизации в интернет магазине "):
        page.open_shop()
    with allure.step("авторизовываемся"):
        page.authorization()
    with allure.step("Добавляем три товара в корзину "):
        page.shop_tri()
    with allure.step("Вводим персональные данные"):
        page.personal_data_user()
    with allure.step("Проверяем что цена соответствует значению 58.29"):
        assert page.result_page() == "Total: $58.29"
