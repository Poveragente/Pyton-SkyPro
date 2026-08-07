import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def test_button():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://httpbin.qa-territory.online/forms/post")
    time.sleep(2)

    element = driver.find_element(By.NAME, "custname")
    element.click()
    element.clear()
    element.send_keys("German")
    time.sleep(2)

    element = driver.find_element(By.XPATH, "//button[text()='Submit order']")
    element.click()

    assert (
            "forms/post" not in driver.current_url
    ), "Форма не была отправлена: URL не изменился"

    driver.quit()


if __name__ == "__main__":
    test_button()
