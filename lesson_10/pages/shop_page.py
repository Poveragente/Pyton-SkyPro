import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ShopPage:
    """
    Страница магазина (SauceDemo) для автоматизации через Selenium.
    Класс инкапсулирует локаторы и методы для авторизации,
    добавления товаров в корзину,
    оформления заказа и получения итоговой стоимости.
    """
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

    def __init__(self, driver: webdriver.Remote, url: str) -> None:
        """Инициализирует страницу магазина.
        Args:
            driver: Экземпляр WebDriver для управления браузером.
            url: URL страницы магазина.
        """
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(self.driver, 10)

    @allure.title("Открытие страницы магазина")
    def open_shop(self) -> None:
        """Открывает страницу магазина по заданному URL."""
        self.driver.get(self.url)

    @allure.title("Авторизация")
    def authorization(self) -> None:
        """
        Выполняет авторизацию с тестовыми учётными данными.
        Использует жёстко заданные
        логин/пароль (standard_user / secret_sauce).
        """
        with (allure.step("Находим поле предназначенное для логина,"
                          "проверяем что оно кликабельно")):
            login_field = self.wait.until
            (EC.element_to_be_clickable(self.LOGIN_FIELD))
        with allure.step("очищаем поле"):
            login_field.clear()
        with allure.step("заполняем поле Логин"):
            login_field.send_keys("standard_user")

        with (allure.step("Находим поле предназначенное для Пароля,"
                          "проверяем что оно кликабельно")):
            password_field = self.wait.until
            (EC.element_to_be_clickable(self.PASSWORD_FIELD))
        with allure.step("очищаем поле"):
            password_field.clear()
        with allure.step("заполняем поле пароль"):
            password_field.send_keys("secret_sauce")
        with (allure.step("проверяем что кнопка Залогинится активна, "
                          "прокликиваем её")):
            login_btn = self.wait.until
            (EC.element_to_be_clickable(self.LOGIN_BUTTON))
            login_btn.click()

    @allure.title("Добавление товаров в корзину")
    def shop_tri(self) -> None:
        """
        Добавляет в корзину три заранее определённых товара
        и переходит к оформлению заказа.
        Товары: Backpack, Bolt T-Shirt, Onesie.
        """
        products_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        for product_name in products_to_add:
            with allure.step("Поиск товаров по названию из списка"):
                product_card = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH,
                         f"//div[@class="
                         f"'inventory_item']//div[text()='{product_name}']"
                         f"/ancestor::div[@class='inventory_item']")
                    )
                )
            with (allure.step("Прокликиваем мышью по товару "
                              "добавляя его в корзину")):
                add_btn = product_card.find_element
                (By.CSS_SELECTOR, "button.btn_primary")
                add_btn.click()
        with (allure.step("Находим элемент корзина,"
                          " проверяем что он виден")):
            cart_badge = self.wait.until
            (EC.visibility_of_element_located(self.CART_BADGE))
        with allure.step("Кликаем на корзину"):
            cart_badge.click()
        with (allure.step("Проверяем что кнопка продолжить"
                          " кликабельна")):
            checkout_link = self.wait.until
            (EC.element_to_be_clickable(self.CHECKOUT_LINK))
        with allure.step("Прокликиваем мышью по "
                         "кнопке продолжить"):
            checkout_link.click()

    @allure.title("Заполнение персональных данных")
    def personal_data_user(self) -> None:
        """
        Заполняет форму персональных данных
        тестовыми значениями.
        Имя: GERMAN, Фамилия: JACK, Почтовый индекс: 123456.
        """
        with (((allure.step("Находим поле имя")))):
            first_name_field = self.wait.until
            (EC.element_to_be_clickable(self.FIRST_NAME_FIELD))
        with allure.step("очищаем поле"):
            first_name_field.clear()
        with allure.step("Вводим значение"):
            first_name_field.send_keys("GERMAN")

        with (allure.step("Находим поле фамилия")):
            last_name_field = self.wait.until
            (EC.element_to_be_clickable(self.LAST_NAME_FIELD))
        with allure.step("очищаем поле"):
            last_name_field.clear()
        with allure.step("Вводим значение"):
            last_name_field.send_keys("JACK")

        with (allure.step("Находим поле zip-code")):
            zip_code_field = self.wait.until
            (EC.element_to_be_clickable(self.ZIP_CODE_FIELD))
        with allure.step("очищаем поле"):
            zip_code_field.clear()
        with allure.step("Вводим значение"):
            zip_code_field.send_keys("123456")

        with (allure.step("Находим кнопку Продолжить")):
            continue_btn = self.wait.until
            (EC.element_to_be_clickable(self.CONTINUE_BUTTON))
        with allure.step("Прокликиваем её"):
            continue_btn.click()

    @allure.title("Возвращает общую цену товара")
    def result_page(self) -> str:
        """Ожидает появления и возвращает текст с итоговой стоимостью заказа.
            Returns:
            Текст элемента с итоговой стоимостью (например, "$57.34").
        """
        total_price_label = (self.wait.until(EC.visibility_of_element_located
                                             (self.TOTAL_PRICE_LABEL)))
        return total_price_label.text
