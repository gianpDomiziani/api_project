import contextlib
import sqlite3

def start_db(url):
    return sqlite3.connect(url)

def close_db(session):
    return session.close()


@contextlib.contextmanager
def dbhandler(url):
    session =start_db(url)
    yield session
    close_db(session)
