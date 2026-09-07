from t08_lesson.pages.project_page import ProjectPage


def test_get_project_by_id(token, base_url):
    page = ProjectPage(base_url, token)
    unique_title = "Umbrella-3"
    project_id = None

    try:
        # 1. Создаём проект
        resp_create = page.create_project(unique_title)
        assert resp_create.status_code == 201, (
            f"Ожидался 201 при создании, получен {resp_create.status_code}"
        )

        created = resp_create.json()
        assert "id" in created, "В ответе на создание нет поля 'id'"
        project_id = created["id"]
        print(f"✅ Проект создан: ID={project_id}")

        # 2. Получаем проект по ID
        resp_get = page.get_project(project_id)
        assert resp_get.status_code == 200, (
            f"Ожидался 200 при GET, получен {resp_get.status_code}. "
            f"Тело: {resp_get.text}"
        )

        retrieved = resp_get.json()

        # 3. Проверки
        assert retrieved is not None, "Ответ на GET-запрос пустой"
        assert "id" in retrieved, "В GET-ответе нет поля 'id'"
        assert retrieved["id"] == project_id, "ID не совпадает"
        assert "title" in retrieved, "В GET-ответе нет поля 'title'"
        assert retrieved["title"] == unique_title, (
            f"Название не совпадает: ожидалось {unique_title}, "
            f"получено {retrieved['title']}"
        )

        print(f"✅ Проект получен: ID={retrieved['id']}, Title={retrieved['title']}")

    finally:
        if project_id:
            page.delete_project(project_id)
            print(f"🧹 Проект удалён: ID={project_id}")
