import pytest
from selenium import webdriver
from pages.shop_page import ShopPage


@pytest.fixture
def driver():
    drv = webdriver.Chrome()
    yield drv
    drv.quit()


def test_shop_flow(driver):
    page = ShopPage(driver, "https://www.saucedemo.com/")
    page.open_shop()
    page.authorization()
    page.shop_tri()
    page.personal_data_user()
    assert page.result_page() == "Total: $58.29"
