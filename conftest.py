import pytest
import requests

from t08_lesson.pages.project_page import ProjectPage


@pytest.fixture(scope="session")
def base_url():
    return "https://ru.yougile.com"


@pytest.fixture(scope="session")
def auth_credentials():
    return {
        "login": "YOUR_LOGIN",  # --Вставьте сюда ваш логин от yougile
        "password": "YOUR_PASSWORD",  # -- Вставьте сюда ваш пароль от yougile
        "name": "Аларм Тест",
    }


@pytest.fixture(scope="session")
def token(auth_credentials, base_url):
    data = {
        "login": auth_credentials["login"],
        "password": auth_credentials["password"],
    }
    url = f"{base_url}/api-v2/auth/keys/get"
    print(f"🚀 Запрос токена: {url}")

    resp = requests.post(url, json=data, timeout=10)
    if resp.status_code != 200:
        pytest.fail(f"Auth failed: {resp.status_code} | {resp.text[:200]}")

    result = resp.json()

    def find_token_entry(obj):
        if isinstance(obj, dict):
            if "key" in obj:
                return obj
            for v in obj.values():
                r = find_token_entry(v)
                if r:
                    return r
        elif isinstance(obj, list):
            for item in obj:
                r = find_token_entry(item)
                if r:
                    return r
        return None

    entry = find_token_entry(result)
    if not entry:
        pytest.fail("Token not found in auth response")

    print("✅ Токен получен")
    return entry["key"]


@pytest.fixture(scope="session")
def page(base_url, token):
    return ProjectPage(base_url, token)


@pytest.fixture(scope="session")
def company_id(page):
    cid = page.get_company_id()
    print(f"✅ Получен company_id: {cid}")
    return cid
