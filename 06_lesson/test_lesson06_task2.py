from selenium import webdriver
import time


def test_session_storage_auth():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://gitflic.ru/user/gerdolf")
    url_user1 = driver.current_url

    # передаем токен авторизации
    driver.add_cookie(
        {
            "name": "SESSION",
            "value": "Подставьте сюда значения вашего токена для User 1",
            "domain": "gitflic.ru",
        }
    )
    # Обновляем страницу
    driver.refresh()
    # Очищаем куки
    driver.delete_all_cookies()
    driver.refresh()

    driver.add_cookie(
        {
            "name": "SESSION",
            "value": "Подставьте сюда значения вашего токена для User 2",
            "domain": "gitflic.ru",
        }
    )
    driver.refresh()
    driver.get("https://gitflic.ru/user/povera_gente")
    url_user2 = driver.current_url

    assert url_user1 != url_user2, "Тест не пройден URL не отличаются"

    driver.delete_all_cookies()
    driver.refresh()
    time.sleep(5)

    driver.quit()


if __name__ == "__main__":
    test_session_storage_auth()
