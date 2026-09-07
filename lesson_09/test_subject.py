import pytest
from subject_bd import SubjectsTable

DB_CONNECTION_STRING = "postgresql://postgres:123@127.0.0.1:5432/QA134"
db = SubjectsTable(DB_CONNECTION_STRING)


@pytest.fixture
def create_test_subject():
    subject_id = db.get_next_id()
    subject_title = f"Тестовый предмет {subject_id}"

    db.create_subject(subject_id, subject_title)

    yield {"subject_id": subject_id, "subject_title": subject_title}

    # Очистка после теста
    db.delete_subject(subject_id)


class TestSubjectsCRUD:

    def test_create_subject(self, create_test_subject):
        row = db.get_subject(create_test_subject["subject_id"])

        # Сначала проверяем, что запись вообще нашлась
        assert (
            row is not None
        ), f"Не удалось найти предмет с ID {create_test_subject['subject_id']}"

        # Теперь безопасно обращаемся по ключам, так как row — это обычный dict
        assert row["subject_id"] == create_test_subject["subject_id"]
        assert row["subject_title"] == create_test_subject["subject_title"]

    def test_update_subject(self, create_test_subject):
        new_title = "Обновлённое название предмета"
        db.update_subject(create_test_subject["subject_id"], new_title)

        row = db.get_subject(create_test_subject["subject_id"])
        assert row is not None
        assert row["subject_title"] == new_title

    def test_delete_subject(self, create_test_subject):
        subject_id = create_test_subject["subject_id"]
        db.delete_subject(subject_id)

        # После удаления запись должна отсутствовать
        row = db.get_subject(subject_id)
        assert row is None
