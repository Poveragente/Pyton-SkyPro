import pytest
from students_db import StudentTable

DB_CONNECTION_STRING = "postgresql://postgres:123@127.0.0.1:5432/QA134"
db = StudentTable(DB_CONNECTION_STRING)


@pytest.fixture
def create_test_student():
    user_id = db.get_next_id()
    level = "Junior"
    education_form = "Full-time"
    subject_id = 1

    db.create_student(user_id, level, education_form, subject_id)

    yield {
        "user_id": user_id,
        "level": level,
        "education_form": education_form,
        "subject_id": subject_id,
    }

    db.delete_student(user_id)


class TestStudentsCRUD:
    def test_create_student(self, create_test_student):
        row = db.get_student(create_test_student["user_id"])
        assert row is not None
        assert row["user_id"] == create_test_student["user_id"]
        assert row["level"] == create_test_student["level"]
        assert row["education_form"] == create_test_student["education_form"]
        assert row["subject_id"] == create_test_student["subject_id"]

    def test_update_student(self, create_test_student):
        new_level = "Senior"
        new_education_form = "Part-time"
        new_subject_id = 2

        db.update_student(
            create_test_student["user_id"],
            new_level,
            new_education_form,
            new_subject_id,
        )

        row = db.get_student(create_test_student["user_id"])
        assert row is not None
        assert row["level"] == new_level
        assert row["education_form"] == new_education_form
        assert row["subject_id"] == new_subject_id

    def test_delete_student(self, create_test_student):
        user_id = create_test_student["user_id"]
        db.delete_student(user_id)
        row = db.get_student(user_id)
        assert row is None
