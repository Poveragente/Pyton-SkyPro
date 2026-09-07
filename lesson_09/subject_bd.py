from sqlalchemy import create_engine, text


class SubjectsTable:
    __scripts = {
        "select by id": text(
            "SELECT subject_id, subject_title FROM subject WHERE subject_id = :id " 
            ""
        ),
        "insert": text("""
            INSERT INTO subject (subject_id, subject_title)
            VALUES (:id, :title)
            RETURNING subject_id, subject_title
        """),
        "update": text("""
            UPDATE subject
            SET subject_title = :title
            WHERE subject_id = :id
        """),
        "delete": text("DELETE FROM subject WHERE subject_id = :id"),
        "get next id": text(
            "SELECT COALESCE(MAX(subject_id), 0)" " " "+ 1 AS next_id FROM subject"
        ),
    }

    def __init__(self, connection_string):
        self.__db = create_engine(connection_string)

    def get_subject(self, subject_id: int):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["select by id"],
                                  {"id": subject_id})
            # fetchone() возвращает одну строку (или None), если ничего не найдено
            row = result.fetchone()

            if row is None:
                return None

            # Явно собираем словарь. Это защищает от любых странных багов mappings()
            return {"subject_id": row.subject_id,
                    "subject_title": row.subject_title}

    def create_subject(self, subject_id: int, subject_title: str):
        with self.__db.begin() as conn:
            result = conn.execute(
                self.__scripts["insert"],
                {"id": subject_id, "title": subject_title},
            )
            row = result.fetchone()
            if row is None:
                return None
            return {"subject_id": row.subject_id,
                    "subject_title": row.subject_title}

    def update_subject(self, subject_id: int, subject_title: str):
        with self.__db.begin() as conn:
            conn.execute(
                self.__scripts["update"],
                {"id": subject_id, "title": subject_title},
            )

    def delete_subject(self, subject_id: int):
        with self.__db.begin() as conn:
            conn.execute(self.__scripts["delete"],
                         {"id": subject_id})

    def get_next_id(self):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["get next id"])
            val = result.scalar()
            # Если таблица пустая, MAX вернет NULL, COALESCE сделает 0, +1 даст 1
            return (val or 0) + 1
