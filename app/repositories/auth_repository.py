from app.models.user_model import User

class SQLiteRepository:

    def __init__(self, session):
        self._session = session
        self._cursor = session.cursor()
    
    def get_user(self, username):
        return self._cursor.execute("SELECT * FROM user WHERE username=?", (username,)).fetchone()

    def kickoff_user(self):
        pass

    def new_user(self, username, password):
        self._cursor.execute(""" INSERT INTO user(USERNAME, PASSWORD) VALUES (?,?) """, (username, password))

    def get_id_from_user(self, username):
        user = self._cursor.execute("SELECT * FROM user WHERE username=?", (username,)).fetchone()
        if user:
            return user[0]
        return None
    
    def get_user_from_id(self, id):
        user = self._cursor.execute("SELECT * FROM user WHERE id=?", (id,)).fetchone()
        if user:
            # return user id and username.
            return (user[0], user[1])
        return None