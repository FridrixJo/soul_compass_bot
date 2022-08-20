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

    def set_first_rate_name(self, first_rate_name, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET first_rate_name = ? WHERE id = ?", (first_rate_name, id))
        except Exception as e:
            print(e, "set_first_rate_name")
        return self.db.commit()

    def get_first_rate_name(self, id=1):
        try:
            result = self.sql.execute("SELECT first_rate_name FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_first_rate_name")

    def set_first_rate_descr(self, first_rate_descr, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET first_rate_descr = ? WHERE id = ?", (first_rate_descr, id))
        except Exception as e:
            print(e, "set_first_rate_descr")
        return self.db.commit()

    def get_first_rate_descr(self, id=1):
        try:
            result = self.sql.execute("SELECT first_rate_descr FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_first_rate_descr")

    def set_second_rate_name(self, second_rate_name, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET second_rate_name = ? WHERE id = ?", (second_rate_name, id))
        except Exception as e:
            print(e, "set_first_rate_name")
        return self.db.commit()

    def get_second_rate_name(self, id=1):
        try:
            result = self.sql.execute("SELECT second_rate_name FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_second_rate_name")

    def set_second_rate_descr(self, second_rate_descr, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET second_rate_descr = ? WHERE id = ?", (second_rate_descr, id))
        except Exception as e:
            print(e, "set_second_rate_descr")
        return self.db.commit()

    def get_second_rate_descr(self, id=1):
        try:
            result = self.sql.execute("SELECT second_rate_descr FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_second_rate_descr")

    def set_third_rate_name(self, third_rate_name, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET third_rate_name = ? WHERE id = ?", (third_rate_name, id))
        except Exception as e:
            print(e, "set_third_rate_name")
        return self.db.commit()

    def get_third_rate_name(self, id=1):
        try:
            result = self.sql.execute("SELECT third_rate_name FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_third_rate_name")

    def set_third_rate_descr(self, third_rate_descr, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET third_rate_descr = ? WHERE id = ?", (third_rate_descr, id))
        except Exception as e:
            print(e, "set_third_rate_descr")
        return self.db.commit()

    def get_third_rate_descr(self, id=1):
        try:
            result = self.sql.execute("SELECT third_rate_descr FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_third_rate_descr")

    def set_first_rate_price(self, first_rate_price, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET first_rate_price = ? WHERE id = ?", (first_rate_price, id))
        except Exception as e:
            print(e, "set_first_rate_price")
        return self.db.commit()

    def get_first_rate_price(self, id=1):
        try:
            result = self.sql.execute("SELECT first_rate_price FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_first_rate_price")

    def set_second_rate_price(self, second_rate_price, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET second_rate_price = ? WHERE id = ?", (second_rate_price, id))
        except Exception as e:
            print(e, "set_second_rate_price")
        return self.db.commit()

    def get_second_rate_price(self, id=1):
        try:
            result = self.sql.execute("SELECT second_rate_price FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_second_rate_price")

    def set_third_rate_price(self, third_rate_price, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET third_rate_price = ? WHERE id = ?", (third_rate_price, id))
        except Exception as e:
            print(e, "set_third_rate_price")
        return self.db.commit()

    def get_third_rate_price(self, id=1):
        try:
            result = self.sql.execute("SELECT third_rate_price FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_third_rate_price")

    def set_first_rate_conditions(self, first_rate_conditions, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET first_rate_conditions = ? WHERE id = ?", (first_rate_conditions, id))
        except Exception as e:
            print(e, "set_first_rate_conditions")
        return self.db.commit()

    def get_first_rate_conditions(self, id=1):
        try:
            result = self.sql.execute("SELECT first_rate_conditions FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_first_rate_conditions")

    def set_second_rate_conditions(self, second_rate_conditions, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET second_rate_conditions = ? WHERE id = ?", (second_rate_conditions, id))
        except Exception as e:
            print(e, "set_second_rate_conditions")
        return self.db.commit()

    def get_second_rate_conditions(self, id=1):
        try:
            result = self.sql.execute("SELECT second_rate_conditions FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_second_rate_conditions")

    def set_third_rate_conditions(self, third_rate_conditions, id=1):
        try:
            self.sql.execute("UPDATE `statements` SET third_rate_conditions = ? WHERE id = ?", (third_rate_conditions, id))
        except Exception as e:
            print(e, "set_third_rate_conditions")
        return self.db.commit()

    def get_third_rate_conditions(self, id=1):
        try:
            result = self.sql.execute("SELECT third_rate_conditions FROM statements WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_third_rate_conditions")



