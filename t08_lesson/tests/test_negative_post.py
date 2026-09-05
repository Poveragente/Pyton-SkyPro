import pytest
from t08_lesson.pages.project_page import ProjectPage


def test_create_project_empty_title(token, base_url):
    """Создание проекта с пустым title — ожидаем 400"""
    page = ProjectPage(base_url, token)
    resp = page.create_project_raw({"title": ""})

    assert resp.status_code == 400, (
        f"Ожидался 400 при пустом title, получен {resp.status_code}. "
        f"Ответ: {resp.text}"
    )
    print(f"✅ Пустой title отклонён: status={resp.status_code}")


def test_create_project_missing_title_field(token, base_url):
    """Создание проекта без поля title — ожидаем 400"""
    page = ProjectPage(base_url, token)
    resp = page.create_project_raw({})

    assert resp.status_code == 400, (
        f"Ожидался 400 без поля title, получен {resp.status_code}. "
        f"Ответ: {resp.text}"
    )
    print(f"✅ Отсутствие title отклонено: status={resp.status_code}")


def test_create_project_null_title(token, base_url):
    """Создание проекта с title=null — ожидаем 400"""
    page = ProjectPage(base_url, token)
    resp = page.create_project_raw({"title": None})

    assert resp.status_code == 400, (
        f"Ожидался 400 при title=null, получен {resp.status_code}. "
        f"Ответ: {resp.text}"
    )
    print(f"✅ title=null отклонён: status={resp.status_code}")
