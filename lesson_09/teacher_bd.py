from sqlalchemy import create_engine, text


class TeacherTable:
    __scripts = {
        "select by id": text(
            "SELECT teacher_id, email," " group_id "
            "FROM teacher WHERE teacher_id = :id"
        ),
        "insert": text("""
            INSERT INTO teacher (teacher_id, email, group_id)
            VALUES (:id, :email, :group_id)
            RETURNING teacher_id, email, group_id
        """),
        "update": text("""
            UPDATE teacher
            SET email = :email, group_id = :group_id
            WHERE teacher_id = :id
        """),
        "delete": text("DELETE FROM teacher "
                       "WHERE teacher_id = :id"),
        "get next id": text(
            "SELECT COALESCE(MAX(teacher_id), 0)" " "
            "+ 1 AS next_id FROM teacher"
        ),
    }

    def __init__(self, connection_string):
        self.__db = create_engine(connection_string)

    def get_teacher(self, teacher_id: int):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["select by id"],
                                  {"id": teacher_id})
            row = result.fetchone()

            if row is None:
                return None

            return {
                "teacher_id": row.teacher_id,
                "email": row.email,
                "group_id": row.group_id,
            }

    def create_teacher(self, teacher_id: int,
                       email: str, group_id: int):
        with self.__db.begin() as conn:
            result = conn.execute(
                self.__scripts["insert"],
                {"id": teacher_id, "email": email,
                 "group_id": group_id},
            )
            row = result.fetchone()
            if row is None:
                return None
            return {
                "teacher_id": row.teacher_id,
                "email": row.email,
                "group_id": row.group_id,
            }

    def update_teacher(self, teacher_id: int,
                       email: str, group_id: int):
        with self.__db.begin() as conn:
            conn.execute(
                self.__scripts["update"],
                {"id": teacher_id,
                 "email": email, "group_id": group_id},
            )

    def delete_teacher(self, teacher_id: int):
        with self.__db.begin() as conn:
            conn.execute(self.__scripts["delete"],
                         {"id": teacher_id})

    def get_next_id(self):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["get next id"])
            val = result.scalar()
            return (val or 0) + 1
