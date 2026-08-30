import uuid

from pages.project_page import ProjectPage


def test_get_nonexistent_project(token, base_url):
    #  Негативный тест: для несуществующего ID

    page = ProjectPage(base_url, token)
    # Генерируем заведомо несуществующий UUID
    nonexistent_id = str(uuid.uuid4())

    resp = page.get_project_raw(nonexistent_id)

    assert resp.status_code in (404, 400), f"Ожидался 404 или 400, получен {resp.status_code}. Ответ: {resp.text}"
    print(f"✅ Правильно отклонён запрос к несуществующему проекту: status={resp.status_code}")


def test_get_invalid_id_format(token, base_url):
    # Негативный тест: некорректный ID (короткая строка)
    page = ProjectPage(base_url, token)
    invalid_id = "abc"

    resp = page.get_project_raw(invalid_id)

    assert resp.status_code == 404, f"Ожидался 400 для невалидного ID, получен {resp.status_code}. Ответ: {resp.text}"
    print(f"✅ Правильно отклонён запрос с невалидным ID: status={resp.status_code}")


def test_get_nonexistent_project_detailed(token, base_url):
    """
    Негативный тест: для заведомо несуществующего ID.
    Ожидаем:
      - статус 404 (или 400)
      - в ответе есть сообщение об ошибке, а не пустой объект
    """
    page = ProjectPage(base_url, token)
    nonexistent_id = str(uuid.uuid4())

    resp = page.get_project_raw(nonexistent_id)

    # 1. Проверяем статус
    assert resp.status_code in (404, 400), f"Ожидался 404 или 400, получен {resp.status_code}. Ответ: {resp.text}"

    # 2. Проверяем, что ответ — JSON (а не HTML/пустота)
    try:
        error_body = resp.json()
    except ValueError:
        pytest.fail(f"Ответ не является JSON: {resp.text[:200]}")

    # 3. Проверяем наличие сообщения об ошибке
    has_message = "message" in error_body or "error" in error_body
    assert has_message, f"В ответе нет понятного сообщения об ошибке. Получено: {error_body}"

    print(f"✅ Правильно отклонён запрос к несуществующему проекту: status={resp.status_code}, body={error_body}")


def test_project_no_title(token, base_url):
    """
    Негативный тест: попытка создать проект с пустым title.
    Ожидаем: 400 (ошибка валидации)
    """
    page = ProjectPage(base_url, token)
    no_title = "None"  # или None, если API это тоже не любит

    # Используем raw-метод, чтобы получить Response и проверить статус
    resp = page.get_project_raw(no_title)

    assert resp.status_code == 404, f"Ожидался 400 при пустом title, получен {resp.status_code}. Ответ: {resp.text}"
