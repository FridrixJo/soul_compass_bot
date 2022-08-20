import sqlite3


class UsersDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def user_exists(self, user_id):
        try:
            result = self.sql.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
            return bool(len(result.fetchall()))
        except Exception as s:
            print(s, "user_exists")

    def add_user(self, user_id, name, type='simple'):
        try:
            self.sql.execute("INSERT INTO `users` (`user_id`, `name`, `type`) VALUES (?, ?, ?)", (user_id, name, type))
        except Exception as e:
            print(e, "add_user")
        return self.db.commit()

    def get_users(self):
        try:
            result = self.sql.execute("SELECT `user_id` FROM `users`")
            return result.fetchall()
        except Exception as s:
            print(type(s))

    def get_users_by_type(self, type):
        try:
            result = self.sql.execute("SELECT `user_id` FROM `users` WHERE type = ?", (type,))
            return result.fetchall()
        except Exception as s:
            print(type(s))

    def delete_user(self, user_id):
        try:
            self.sql.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        except Exception as e:
            pass
        return self.db.commit()

    def delete_all(self):
        user_list = self.get_users()
        print(user_list)
        try:
            for i in user_list:
                self.delete_user(i[0])
        except Exception as e:
            print(e)
        return self.db.commit()

    def set_name(self, user_id, name):
        try:
            self.sql.execute("UPDATE `users` SET name = ? WHERE user_id = ?", (name, user_id))
        except Exception as e:
            print(e, "name")
        return self.db.commit()

    def get_name(self, user_id):
        try:
            result = self.sql.execute("SELECT name FROM users WHERE user_id = ?", (user_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_name")

    def set_type(self, user_id, type):
        try:
            self.sql.execute("UPDATE `users` SET type = ? WHERE user_id = ?", (type, user_id))
        except Exception as e:
            print(e, "type")
        return self.db.commit()

    def get_type(self, user_id):
        try:
            result = self.sql.execute("SELECT type FROM users WHERE user_id = ?", (user_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_type")
