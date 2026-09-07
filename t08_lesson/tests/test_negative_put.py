import uuid
from t08_lesson.pages.project_page import ProjectPage


def test_update_nonexistent_project(token, base_url):
    """Обновление несуществующего проекта — ожидаем 404 или 400"""
    page = ProjectPage(base_url, token)
    fake_id = str(uuid.uuid4())

    resp = page.update_project_raw(fake_id, {"title": "Ghost"})

    assert resp.status_code in (404, 400), (
        f"Ожидался 404 или 400, получен {resp.status_code}. "
        f"Ответ: {resp.text}"
    )
    print(f"✅ Обновление несуществующего проекта отклонено: status={resp.status_code}")


def test_update_project_empty_title(token, base_url):
    """Обновление проекта с пустым title — ожидаем 400"""
    page = ProjectPage(base_url, token)
    project_id = None

    try:
        # Сначала создаём реальный проект
        resp_create = page.create_project("TempForNegativePUT")
        assert resp_create.status_code == 201
        project_id = resp_create.json()["id"]

        # Пытаемся обновить с пустым title
        resp = page.update_project_raw(project_id, {"title": ""})

        assert resp.status_code == 400, (
            f"Ожидался 400 при пустом title, получен {resp.status_code}. "
            f"Ответ: {resp.text}"
        )
        print(f"✅ Пустой title при PUT отклонён: status={resp.status_code}")

    finally:
        if project_id:
            page.delete_project(project_id)

