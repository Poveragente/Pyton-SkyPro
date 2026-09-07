from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CalsPage:
    DELAY_INPUT = (By.ID, "delay")
    CHISLO_ONE = (By.XPATH, "//span[contains(text(), '7')]")
    OPERATOR_PLUS = (By.XPATH, "//span[contains(text(), '+')]")
    CHISLO_TWO = (By.XPATH, "//span[contains(text(), '8')]")
    OPERATOR_RAVNO = (By.XPATH, "//span[contains(text(), '=')]")
    SCREEN_RES = (By.CLASS_NAME, "screen")

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(self.driver, 60)

    def open_cals(self):
        self.driver.get(self.url)

    def delay_input(self, value="12"):
        delay_input = self.wait.until(EC.element_to_be_clickable(self.DELAY_INPUT))
        delay_input.clear()
        delay_input.send_keys(45)

    def click_btn(self, locator):
        btn = self.wait.until(EC.element_to_be_clickable(locator))
        btn.click()

    def sloshenie(self):
        self.click_btn(self.CHISLO_ONE)
        self.click_btn(self.OPERATOR_PLUS)
        self.click_btn(self.CHISLO_TWO)
        self.click_btn(self.OPERATOR_RAVNO)

    def get_result(self):
        wait = WebDriverWait(self.driver, 60)
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15"))

        result_element = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "screen")))
        return result_element.text

#    def get_result(self):
#        if(self.SCREEN_RES != "15"):
#            wait = WebDriverWait(self.driver, 60)
#            self.SCREEN_RES = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15"))
#            return self.SCREEN_RES
