import sqlite3
from db_utils import dbhandler

with dbhandler() as session:
    cursor = session.cursor()
    # drop table pages if it exists
    cursor.execute("DROP TABLE IF EXISTS pages")
    cursor.execute(""" CREATE TABLE pages
                   (id INTEGER, title TEXT, header TEXT, author TEXT, body TEXT, edit INTEGER) """)
    # save the change and close the session.
    conn.commit()
