from t08_lesson.pages.project_page import ProjectPage

def test_create_project(token, base_url):
    page = ProjectPage(base_url, token)
    unique_title = "Umbrella-AutoTest"
    project_id = None

    try:
        # 1. Создаём проект
        resp_create = page.create_project(unique_title)

        assert resp_create.status_code == 201, (
            f"Ожидался 201 при создании, получен {resp_create.status_code}. "
            f"Тело: {resp_create.text}"
        )

        project_short = resp_create.json()
        assert "id" in project_short, "В ответе нет поля 'id'"
        project_id = project_short["id"]
        print(f"✅ Проект создан: ID={project_id}")

        # 2. Получаем полное описание
        resp_get = page.get_project(project_id)

        assert resp_get.status_code == 200, (
            f"Ожидался 200 при получении, получен {resp_get.status_code}. "
            f"Тело: {resp_get.text}"
        )

        project_full = resp_get.json()
        assert "title" in project_full, "В полном ответе нет поля 'title'"
        assert project_full["title"] == unique_title, (
            f"Название не совпадает: ожидалось {unique_title}, "
            f"получено {project_full['title']}"
        )

        print(f"✅ Название подтверждено: {project_full['title']}")

    finally:
        # Очистка
        if project_id:
            page.delete_project(project_id)
            print(f"🧹 Проект удалён: ID={project_id}")