import sqlite3


class PhotosDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def request_exists(self, request_id):
        try:
            result = self.sql.execute("SELECT `id` FROM `photos` WHERE `request_id` = ?", (request_id,))
            return bool(len(result.fetchall()))
        except Exception as s:
            print(s, "request_exists")

    def user_exists(self, user_id):
        try:
            result = self.sql.execute("SELECT `id` FROM `photos` WHERE `user_id` = ?", (user_id,))
            return bool(len(result.fetchall()))
        except Exception as s:
            print(s, "user_exists")

    def add_request(self, request_id):
        try:
            self.sql.execute("INSERT INTO `photos` (`request_id`) VALUES (?)", (request_id,))
        except Exception as e:
            print(e, "request_id")
        return self.db.commit()

    def get_requests(self):
        try:
            result = self.sql.execute("SELECT `request_id` FROM `photos`")
            return result.fetchall()
        except Exception as s:
            print(type(s))

    def delete_request(self, request_id):
        try:
            self.sql.execute("DELETE FROM photos WHERE request_id = ?", (request_id,))
        except Exception as e:
            pass
        return self.db.commit()

    def delete_all(self):
        request_list = self.get_requests()
        print(request_list)
        try:
            for i in request_list:
                self.delete_request(i[0])
        except Exception as e:
            print(e)
        return self.db.commit()

    def set_user_id(self, request_id, user_id):
        try:
            self.sql.execute("UPDATE `photos` SET user_id = ? WHERE request_id = ?", (user_id, request_id))
        except Exception as e:
            print(e, "set_user_id")
        return self.db.commit()

    def get_user_id(self, request_id):
        try:
            result = self.sql.execute("SELECT user_id FROM photos WHERE request_id = ?", (request_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_user_id")

    def set_name(self, request_id, name):
        try:
            self.sql.execute("UPDATE `photos` SET name = ? WHERE request_id = ?", (name, request_id))
        except Exception as e:
            print(e, "name")
        return self.db.commit()

    def get_name(self, request_id):
        try:
            result = self.sql.execute("SELECT name FROM photos WHERE request_id = ?", (request_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_name")

    def set_type(self, request_id, type):
        try:
            self.sql.execute("UPDATE `photos` SET type = ? WHERE request_id = ?", (type, request_id))
        except Exception as e:
            print(e, "type")
        return self.db.commit()

    def get_type(self, request_id):
        try:
            result = self.sql.execute("SELECT type FROM photos WHERE request_id = ?", (request_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_type")
