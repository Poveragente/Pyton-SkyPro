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
        self.url_auth = f"{self.base_url}/api-v2"

    # --- Служебные ---

    def get_company_id(self):
        url = f"{self.url_auth}/companies"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        companies = data if isinstance(data, list) else [data]

        if not companies:
            raise ValueError("Список компаний пуст — нет доступа ни к одной компании")

        company = companies[0]
        if "id" not in company:
            raise ValueError("В данных компании нет поля 'id'")

        return company["id"]

    # --- Позитивные методы (возвращают Response) ---

    def create_project(self, title):
        """POST /projects — возвращает Response"""
        payload = {"title": title}
        return requests.post(self.url_base, headers=self.headers, json=payload, timeout=10)

    def get_project(self, project_id):
        """GET /projects/{id} — возвращает Response"""
        url = f"{self.url_base}/{project_id}"
        return requests.get(url, headers=self.headers, timeout=10)

    def update_project(self, project_id, new_title):
        """PUT /projects/{id} — возвращает Response"""
        payload = {"title": new_title}
        url = f"{self.url_base}/{project_id}"
        return requests.put(url, headers=self.headers, json=payload, timeout=10)

    def delete_project(self, project_id):
        """DELETE /projects/{id} — возвращает Response"""
        url = f"{self.url_base}/{project_id}"
        return requests.delete(url, headers=self.headers, timeout=10)

    # --- Raw-методы для негативных тестов ---

    def create_project_raw(self, payload):
        """POST /projects с произвольным payload — для негативных тестов"""
        return requests.post(self.url_base, headers=self.headers, json=payload, timeout=10)

    def update_project_raw(self, project_id, payload):
        """PUT /projects/{id} с произвольным payload — для негативных тестов"""
        url = f"{self.url_base}/{project_id}"
        return requests.put(url, headers=self.headers, json=payload, timeout=10)

    def get_project_raw(self, project_id):
        """GET /projects/{id} — сырой Response для негативных тестов"""
        url = f"{self.url_base}/{project_id}"
        return requests.get(url, headers=self.headers, timeout=10)