from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def shop():
    driver = webdriver.Firefox()
    try:
        driver.maximize_window()
        driver.get("https://www.saucedemo.com")

        wait = WebDriverWait(driver, 20)

        login = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
        login.clear()
        login.send_keys("standard_user")

        password = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password.clear()
        password.send_keys("secret_sauce")


        btn = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
        btn.click()

        wait.until(EC.presence_of_element_located((By.ID, "inventory_container")))

        products_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        for product_name in products_to_add:
            product_card = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     f"//div[@class='inventory_item']//div[text()='{product_name}']/ancestor::div[@class='inventory_item']")
                )
            )
            add_btn = product_card.find_element(By.CSS_SELECTOR, "button.btn_primary")
            add_btn.click()

        cart_badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        assert cart_badge.text == "3", f"ожидалось 3 товара в корзине, но было {cart_badge.text}"

        cart_link = driver.find_element(By.CSS_SELECTOR, ".shopping_cart_container a")
        cart_link.click()

        checkout_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_btn.click()

        first_name_input = wait.until(EC.visibility_of_element_located((By.ID, "first-name")))
        last_name_input = wait.until(EC.visibility_of_element_located((By.ID, "last-name")))
        zip_code_input = wait.until(EC.visibility_of_element_located((By.ID, "postal-code")))

        first_name_input.clear()
        first_name_input.send_keys("German")
        last_name_input.clear()
        last_name_input.send_keys("Smith")
        zip_code_input.clear()
        zip_code_input.send_keys("12345")

        continue_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.cart_button"))
        )
        continue_btn.click()

        import time
        sleep(20)

        total_price = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".summary_total_label"))
        )
        total_text = total_price.text.strip()

        if "$" in total_text:
            total_amount = "$" + total_text.split("$")[1].split()[0]
        else:
            raise AssertionError(f"Не удалось найти сумму в формате $X.XX в строке: {total_text}")

        expected_total = "$58.29"
        assert total_amount == expected_total, f"Ожидалось {expected_total}, но получено: {total_amount}"

    finally:
        driver.quit()

if __name__ == '__main__':
    shop()
