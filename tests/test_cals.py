import pytest
from selenium import webdriver

from pages.calc_page import CalsPage


@pytest.fixture
def driver():
    drv = webdriver.Chrome()
    yield drv
    drv.quit()


def test_cals(driver):
    page = CalsPage(driver, "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

    page.open_cals()
    page.delay_input(45)
    page.sloshenie()

    result = page.get_result()
    assert result == "15"
