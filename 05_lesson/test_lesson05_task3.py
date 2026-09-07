import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



def test_multiple_elements(first_link=None):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://httpbin.qa-territory.online/links/10")
    time.sleep(3)

    links = driver.find_elements(By.TAG_NAME, "a")

    assert len(links) == 9, f"Ожидалось 9 ссылок, но найдено: {len(links)}"

    for i, link in enumerate(links):
                EC.visibility_of(link),
                message=f"Ссылка №{i + 1} не отображается на странице"

    first_link_text = links[0].text.strip()
    assert "1" in first_link_text, f"Текст первой ссылки не содержит '1'. Фактический текст: '{first_link_text}'"


if __name__ == "__main__":
    test_multiple_elements()
