import sqlite3
from config import DB_PATH

con = sqlite3.connect(DB_PATH)
cur = con.cursor()


class DB:
    @staticmethod
    def update_user(username, **kwargs):
        username = str(username)
        for key, value in kwargs.items():
            cur.execute(f"UPDATE Users SET {key} = '{value}' WHERE Users.username='{username}';")
        con.commit()

    @staticmethod
    def create_user(username):
        username = str(username)
        con.execute(f"INSERT INTO Users (username) "
                    f"VALUES ('{username}')")

        con.commit()

    @staticmethod
    def get_data():
        cursor = con.execute("SELECT * FROM Users")

        return cursor.fetchall()

    @staticmethod
    def delete_user(username):
        username = str(username)
        con.execute(f"DELETE FROM Users WHERE username='{username}'")

        con.commit()

    @staticmethod
    def get_column(username, column):
        username = str(username)
        cursor = con.execute(f"SELECT {column} FROM Users WHERE username='{username}'")

        return cursor.fetchall()[0][0]

    @staticmethod
    def check_user(username):
        username = str(username)
        cursor = con.execute(f"SELECT * FROM Users WHERE username='{username}'")
        con.close()
        return len(cursor.fetchall()) > 0



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

print(DB.get_data())


#con.close()
