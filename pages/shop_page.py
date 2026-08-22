from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ShopPage:
    LOGIN_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button.btn_primary")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CHECKOUT_LINK = (By.ID, "checkout")
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    ZIP_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    TOTAL_PRICE_LABEL = (By.CLASS_NAME, "summary_total_label")

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(self.driver, 10)

    def open_shop(self):
        self.driver.get(self.url)

    def authorization(self):
        login_field = self.wait.until(EC.element_to_be_clickable(self.LOGIN_FIELD))
        login_field.clear()
        login_field.send_keys("standard_user")

        password_field = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys("secret_sauce")

        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def shop_tri(self):
        products_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        for product_name in products_to_add:
            product_card = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     f"//div[@class='inventory_item']//div[text()='{product_name}']/ancestor::div[@class='inventory_item']")
                )
            )
            add_btn = product_card.find_element(By.CSS_SELECTOR, "button.btn_primary")
            add_btn.click()

        cart_badge = self.wait.until(EC.visibility_of_element_located(self.CART_BADGE))
        cart_badge.click()

        checkout_link = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_LINK))
        checkout_link.click()

    def personal_data_user(self):
        first_name_field = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_FIELD))
        first_name_field.clear()
        first_name_field.send_keys("GERMAN")

        last_name_field = self.wait.until(EC.element_to_be_clickable(self.LAST_NAME_FIELD))
        last_name_field.clear()
        last_name_field.send_keys("JACK")

        zip_code_field = self.wait.until(EC.element_to_be_clickable(self.ZIP_CODE_FIELD))
        zip_code_field.clear()
        zip_code_field.send_keys("123456")

        continue_btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
        continue_btn.click()

    def result_page(self):
        total_price_label = self.wait.until(EC.visibility_of_element_located(self.TOTAL_PRICE_LABEL))
        return total_price_label.text
