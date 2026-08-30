import requests


class ProjectPage:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        self.url_base = f"{self.base_url}/api-v2/projects"

    # --- Позитивные методы ---
    def get_company_id(self):
        url = f"{self.url_auth}/companies"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # API может вернуть список или объект — обработаем оба случая
        companies = data if isinstance(data, list) else [data]

        if not companies:
            raise ValueError("Список компаний пуст — у пользователя нет доступа ни к одной компании")

        company = companies[0]
        return company["id"]

    def create_project(self, title):
        payload = {"title": title}
        resp = requests.post(self.url_base, headers=self.headers, json=payload, timeout=10)
        if resp.status_code != 201:
            print("❌ Ошибка создания проекта:")
            print(f"   Статус: {resp.status_code}")
            print(f"   URL: {self.url_base}")
            print(f"   Payload: {payload}")
            print(f"   Ответ сервера: {resp.text}")
        resp.raise_for_status()
        data = resp.json()
        return data[0] if isinstance(data, list) else data

    def get_project(self, project_id):
        url = f"{self.url_base}/{project_id}"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data[0] if isinstance(data, list) else data

    def update_project(self, project_id, new_title):
        payload = {"title": new_title}
        url = f"{self.url_base}/{project_id}"
        resp = requests.put(url, headers=self.headers, json=payload, timeout=10)
        if resp.status_code not in (200, 204):
            print(f"[ProjectPage] Ошибка обновления: {resp.status_code} | {resp.text}")
        resp.raise_for_status()
        data = resp.json()
        return data[0] if isinstance(data, list) else data

    # --- Методы для негативных тестов (возвращают Response) ---
    def get_project_raw(self, project_id):
        """Возвращает Response целиком — чтобы проверить статус и текст ошибки"""
        url = f"{self.url_base}/{project_id}"
        return requests.get(url, headers=self.headers, timeout=10)
