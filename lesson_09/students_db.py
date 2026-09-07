from sqlalchemy import create_engine, text


class StudentTable:
    __scripts = {
        "select by id": text(
            "SELECT user_id, level, education_form, "
            "subject_id FROM student WHERE user_id = :id"
        ),
        "insert": text("""
            INSERT INTO student (user_id, level,
            education_form, subject_id)
            VALUES (:id, :level, :education_form, :subject_id)
            RETURNING user_id, level, education_form, subject_id
        """),
        "update": text("""
            UPDATE student
            SET level = :level, education_form = :education_form, 
            subject_id = :subject_id
            WHERE user_id = :id
        """),
        "delete": text("DELETE FROM student "
                       "WHERE user_id = :id"),
        "get next id": text(
            "SELECT COALESCE(MAX(user_id), 0)"
            " + 1 AS next_id FROM student"
        ),
    }

    def __init__(self, connection_string):
        self.__db = create_engine(connection_string)

    def get_student(self, user_id: int):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["select by id"],
                                  {"id": user_id})
            row = result.fetchone()
            if row is None:
                return None
            return {
                "user_id": row.user_id,
                "level": row.level,
                "education_form": row.education_form,
                "subject_id": row.subject_id,
            }

    def create_student(
        self, user_id: int, level: str,
            education_form: str, subject_id: int
    ):
        with self.__db.begin() as conn:
            result = conn.execute(
                self.__scripts["insert"],
                {
                    "id": user_id,
                    "level": level,
                    "education_form": education_form,
                    "subject_id": subject_id,
                },
            )
            row = result.fetchone()
            if row is None:
                return None
            return {
                "user_id": row.user_id,
                "level": row.level,
                "education_form": row.education_form,
                "subject_id": row.subject_id,
            }

    def update_student(
        self, user_id: int, level: str,
            education_form: str, subject_id: int
    ):
        with self.__db.begin() as conn:
            conn.execute(
                self.__scripts["update"],
                {
                    "id": user_id,
                    "level": level,
                    "education_form": education_form,
                    "subject_id": subject_id,
                },
            )

    def delete_student(self, user_id: int):
        with self.__db.begin() as conn:
            conn.execute(self.__scripts["delete"],
                         {"id": user_id})

    def get_next_id(self):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["get next id"])
            val = result.scalar()
            return (val or 0) + 1
