import uuid
import pytest
from t08_lesson.pages.project_page import ProjectPage


def test_get_nonexistent_project(token, base_url):
    """GET несуществующего проекта — ожидаем 404 или 400"""
    page = ProjectPage(base_url, token)
    nonexistent_id = str(uuid.uuid4())

    resp = page.get_project_raw(nonexistent_id)

    assert resp.status_code in (404), (
        f"Ожидался 404, получен {resp.status_code}. Ответ: {resp.text}"
    )
    print(f"✅ Несуществующий проект отклонён: status={resp.status_code}")


def test_get_invalid_id_format(token, base_url):
    """GET с некорректным ID — ожидаем 404 или 400"""
    page = ProjectPage(base_url, token)
    invalid_id = "abc"

    resp = page.get_project_raw(invalid_id)

    assert resp.status_code in (404), (
        f"Ожидался 404 для невалидного ID, получен {resp.status_code}. "
        f"Ответ: {resp.text}"
    )
    print(f"✅ Невалидный ID отклонён: status={resp.status_code}")


def test_get_nonexistent_project_has_error_message(token, base_url):
    """GET несуществующего проекта — проверяем, что в ответе есть сообщение об ошибке"""
    page = ProjectPage(base_url, token)
    nonexistent_id = str(uuid.uuid4())

    resp = page.get_project_raw(nonexistent_id)

    assert resp.status_code in (404), (
        f"Ожидался 404, получен {resp.status_code}. Ответ: {resp.text}"
    )

    try:
        error_body = resp.json()
    except ValueError:
        pytest.fail(f"Ответ не является JSON: {resp.text[:200]}")

    has_message = "message" in error_body or "error" in error_body
    assert has_message, f"В ответе нет сообщения об ошибке. Получено: {error_body}"

    print(f"✅ Есть сообщение об ошибке: status={resp.status_code}, body={error_body}")
