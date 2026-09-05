from t08_lesson.pages.project_page import ProjectPage


def test_update_project_title(token, base_url):
    page = ProjectPage(base_url, token)
    unique_title = "Umbrella-Update"
    new_title = "Umbrella_2_Version_2.0"
    project_id = None

    try:
        # 1. Создаём проект
        resp_create = page.create_project(unique_title)
        assert resp_create.status_code == 201, (
            f"Ожидался 201 при создании, получен {resp_create.status_code}. "
            f"Тело: {resp_create.text}"
        )

        project_short = resp_create.json()
        if isinstance(project_short, list):
            project_short = project_short[0]

        assert "id" in project_short, "В ответе на создание нет поля 'id'"
        project_id = project_short["id"]
        print(f"✅ Создан проект: ID={project_id}")

        # 2. Обновляем название
        resp_update = page.update_project(project_id, new_title)
        assert resp_update.status_code in (200, 204), (
            f"Ожидался 200 или 204 при обновлении, получен {resp_update.status_code}. "
            f"Тело: {resp_update.text}"
        )

        # title нужно проверять через GET
        resp_get = page.get_project(project_id)
        assert resp_get.status_code == 200, (
            f"Ожидался 200 при GET, получен {resp_get.status_code}. "
            f"Тело: {resp_get.text}"
        )

        retrieved = resp_get.json()
        if isinstance(retrieved, list):
            retrieved = retrieved[0]

        assert "title" in retrieved, "В GET-ответе нет поля 'title'"
        assert retrieved["title"] == new_title, (
            f"Название не совпадает: ожидалось {new_title}, "
            f"получено {retrieved['title']}"
        )
        print(f"✅ Проект обновлён (через GET): {retrieved['title']}")

    finally:
        if project_id:
            page.delete_project(project_id)
            print(f"🧹 Проект удалён: ID={project_id}")
