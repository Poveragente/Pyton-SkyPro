from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_slow_calc():
    driver = webdriver.Chrome()
    try:
        ##driver.window.maximize_window()
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        wait = WebDriverWait(driver, 60)

        delay_input = wait.until(EC.visibility_of_element_located((By.ID, "delay")))
        delay_input.clear()
        delay_input.send_keys("45")

        buttons = ["7", "+", "8", "="]
        for button in buttons:
            xpath = f"//span[contains(text(), '{button}')]"
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            btn.click()

        result_element = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15"))

        assert result_element == True

    finally:
        driver.quit()


if __name__ == "__main__":
    test_slow_calc()
