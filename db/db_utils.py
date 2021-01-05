import contextlib
import sqlite3

def start_db():
    return sqlite3.connect('../db/page.db')

def close_db(session):
    return session.close()


@contextlib.contextmanager
def dbhandler():
    session =start_db()
    yield session
    close_db(session)
    

