import pytest
from teacher_bd import TeacherTable

DB_CONNECTION_STRING = "postgresql://postgres:123@127.0.0.1:5432/QA134"
db = TeacherTable(DB_CONNECTION_STRING)


@pytest.fixture
def create_test_teacher():
    teacher_id = db.get_next_id()
    email = f"teacher{teacher_id}@example.com"
    group_id = teacher_id  # Для простоты берем тот же ID

    db.create_teacher(teacher_id, email, group_id)

    yield {"teacher_id": teacher_id,
           "email": email, "group_id": group_id}

    # Очистка после теста
    db.delete_teacher(teacher_id)


class TestTeachersCRUD:

    def test_create_teacher(self, create_test_teacher):
        row = db.get_teacher(create_test_teacher["teacher_id"])

        assert (
            row is not None
        ), f"Не удалось найти учителя с ID {create_test_teacher['teacher_id']}"
        assert row["teacher_id"] == create_test_teacher["teacher_id"]
        assert row["email"] == create_test_teacher["email"]
        assert row["group_id"] == create_test_teacher["group_id"]

    def test_update_teacher(self, create_test_teacher):
        new_email = "updated_email@example.com"
        new_group_id = 999

        db.update_teacher(create_test_teacher["teacher_id"],
                          new_email, new_group_id)

        row = db.get_teacher(create_test_teacher["teacher_id"])
        assert row is not None
        assert row["email"] == new_email
        assert row["group_id"] == new_group_id

    def test_delete_teacher(self, create_test_teacher):
        teacher_id = create_test_teacher["teacher_id"]
        db.delete_teacher(teacher_id)

        row = db.get_teacher(teacher_id)
        assert row is None
