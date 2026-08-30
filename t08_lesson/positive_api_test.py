import time
from pages.project_page import ProjectPage

def test_create_project(token, base_url):
    page = ProjectPage(base_url, token)
    unique_title = f"Umbrella-AutoTest"

    # 1. Создаём проект
    project_short = page.create_project(unique_title)

    # Проверяем, что есть ID
    assert "id" in project_short, "В ответе нет поля 'id'"
    project_id = project_short["id"]
    print(f"✅ Проект создан: ID={project_id}")

    # 2. Получаем полное описание
    project_full = page.get_project(project_id)
    assert "title" in project_full, "В полном ответе нет поля 'title'"
    assert project_full["title"] == unique_title, f"Название не совпадает: ожидалось {unique_title}, получено {project_full['title']}"

    print(f"✅ Название подтверждено: {project_full['title']}")


def test_update_project_title(token, base_url):
    page = ProjectPage(base_url, token)

    # 1. Создаём проект
    unique_title = f"Umbrella-Update"
    project_short = page.create_project(unique_title)
    assert "id" in project_short
    project_id = project_short["id"]
    print(f"✅ Создан проект: ID={project_id}")

    # 2. Обновляем название
    new_title = "Umbrella_2_Version_2.0"
    updated = page.update_project(project_id, new_title)

    if "title" not in updated:
        updated = page.get_project(project_id)

    assert updated["title"] == new_title, f"Название не обновилось: ожидалось {new_title}, получено {updated['title']}"
    print(f"✅ Проект успешно обновлён: {updated['title']}")


def test_get_project_by_id(token, base_url):
    page = ProjectPage(base_url, token)
    unique_title = f"Umbrella-3"

    # 1. Создаём проект
    created = page.create_project(unique_title)
    assert "id" in created, "В ответе на создание нет поля 'id'"
    project_id = created["id"]
    print(f"✅ Проект создан: ID={project_id}")

    # 2. Получаем проект по ID
    retrieved = page.get_project(project_id)

    # 3. Проверки
    assert retrieved is not None, "Ответ на GET-запрос пустой"
    assert "id" in retrieved, "В GET-ответе нет поля 'id'"
    assert retrieved["id"] == project_id, "ID в GET-ответе не совпадает с созданным"
    assert "title" in retrieved, "В GET-ответе нет поля 'title'"
    assert retrieved[
               "title"] == unique_title, f"Название не совпадает: ожидалось {unique_title}, получено {retrieved['title']}"

    print(f"✅ Проект успешно получен по ID: {retrieved['id']}, Title={retrieved['title']}")