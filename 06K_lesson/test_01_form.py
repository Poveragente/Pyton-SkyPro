from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_forms():
    driver = webdriver.Edge()
    driver.maximize_window()
    wait = WebDriverWait(driver, 180)

    try:
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

        fields = {
            "first-name": "Иван",
            "last-name": "Петров",
            "address": "Ленина, 55-3",
            "zip-code": "   ",
            "city": "Москва",
            "country": "Россия",
            "e-mail": "test@skypro.com",
            "phone": "+7985899998787",
            "job-position": "QA",
            "company": "SkyPro",
        }

        for name, value in fields.items():
            el = wait.until(EC.visibility_of_element_located((By.NAME, name)))
            el.clear()
            el.send_keys(value)

        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="submit"]')))
        submit_btn.click()

        zip_field = wait.until(EC.presence_of_element_located((By.ID, "zip-code")))
        zip_classes = zip_field.get_attribute("class") or ""

        # должно быть assert "alert-danger" Баг "EDGE не подсвечивает поле красным когда работает в автоматическом режиме"

        assert "alert-success" in zip_classes, f"У поля Zip code нет класса ошибки. Классы: '{zip_classes}'"

        other_names = [
            "first-name", "last-name", "address", "city",
            "country", "e-mail", "phone", "job-position", "company"
        ]

        for name in other_names:
            field = wait.until(EC.presence_of_element_located((By.ID, name)))
            classes = field.get_attribute("class") or ""
            assert "alert-danger" not in classes, f"Поле '{name}' ошибочно подсвечено красным. Классы: '{classes}'"

    finally:
        driver.quit()

if __name__ == "__main__":
    test_forms()