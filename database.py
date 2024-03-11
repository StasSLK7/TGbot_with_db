import sqlite3
from config import DB_PATH




class DB:
    @staticmethod
    def update_user(username, **kwargs):
        con = sqlite3.connect(DB_PATH, check_same_thread=False)
        cur = con.cursor()

        # print(kwargs)
        username = str(username)
        for key, value in kwargs.items():
            cur.execute(f"UPDATE Users SET {key} = '{value}' WHERE username='{username}'")

        con.commit()
        con.close()

    @staticmethod
    def create_user(username):
        con = sqlite3.connect(DB_PATH, check_same_thread=False)
        cur = con.cursor()

        username = str(username)
        con.execute(f"INSERT INTO Users (username) "
                    f"VALUES ('{username}')")

        con.commit()
        con.close()

    @staticmethod
    def get_data():
        con = sqlite3.connect(DB_PATH, check_same_thread=False)
        cur = con.cursor()

        cursor = con.execute("SELECT * FROM Users")

        result = cursor.fetchall()
        con.close()

        return result

    @staticmethod
    def delete_user(username):
        con = sqlite3.connect(DB_PATH, check_same_thread=False)
        cur = con.cursor()

        username = str(username)
        con.execute(f"DELETE FROM Users WHERE username='{username}'")

        con.commit()
        con.close()


    @staticmethod
    def get_column(username, column):
        con = sqlite3.connect(DB_PATH, check_same_thread=False)
        cur = con.cursor()

        username = str(username)
        cursor = con.execute(f"SELECT {column} FROM Users WHERE username='{username}'")

        result = cursor.fetchall()[0][0]
        con.close()
        return result

    @staticmethod
    def check_user(username):
        con = sqlite3.connect(DB_PATH, check_same_thread=False)
        cur = con.cursor()

        username = str(username)
        cursor = con.execute(f"SELECT * FROM Users WHERE username='{username}'")

        result = len(cursor.fetchall()) > 0
        con.close()
        return result




# cur = con.cursor()
#
#
#
# # Сохраняем изменения и закрываем соединение
# con.commit()
#
#
#
# con.close()

# DB.update_user('check',level='yoasdasdasdas123')

print(DB.get_data())

# con.close()
