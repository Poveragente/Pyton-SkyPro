from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_dynamic_loading():
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Переход на страничку
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
    wait = WebDriverWait(driver, 15)

    # Ждём кнопку и кликаем
    start_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Start']"))
    )
    start_btn.click()

    # Ждём появления элемента с текстом «Hello World!»
    hello_el = wait.until(EC.visibility_of_element_located((By.ID, "finish")))
    # Делаем скриншот страницы
    driver.save_screenshot("screenshot.png")
    # Проверяем текст
    assert "Hello World!" in hello_el.text, "Текст 'Hello World!' не появился"

    print("Тест пройден: текст 'Hello World!' появился после загрузки.")

    driver.quit()


if __name__ == "__main__":
    test_dynamic_loading()
