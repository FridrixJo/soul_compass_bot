import sqlite3


class StatementsDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def set_requisites(self, requisites, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET requisites = ? WHERE id = ?", (requisites, id))
        except Exception as e:
            print(e, "set_requisites")
        return self.db.commit()

    def get_requisites(self, id=1):
        try:
            result = self.sql.execute("SELECT requisites FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_requisites")

    def set_questions(self, questions, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET questions = ? WHERE id = ?", (questions, id))
        except Exception as e:
            print(e, "set_questions")
        return self.db.commit()

    def get_questions(self, id=1):
        try:
            result = self.sql.execute("SELECT questions FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_questions")


