import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def test_navigation():
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get("https://httpbin.qa-territory.online")
    time.sleep(3)

    element = driver.find_element(By.LINK_TEXT, "HTML Form")
    element.click()
    time.sleep(3)

    # Проверка, что URL изменился
    assert (
            driver.current_url == "https://httpbin.qa-territory.online/forms/post"
    ), "URL не соответствует ожидаемому"

    driver.back()
    time.sleep(3)
    assert (
            driver.current_url == "https://httpbin.qa-territory.online/"
    ), "URL не соответствует ожидаемому"
    driver.quit()


if __name__ == "__main__":
    test_navigation()
