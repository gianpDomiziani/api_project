import sqlite3

# init a db session
conn = sqlite3.connect('./page.db')
# create a curso object 
cursor = conn.cursor()
# drop table pages if it exists
cursor.execute("DROP TABLE IF EXISTS pages")
# use its execute method for performing the following SQL query
cursor.execute(""" CREATE TABLE pages
                   (id INTEGER, title TEXT, header TEXT, author TEXT, body TEXT, edit INTEGER) """)
# save the change and close the session.
conn.commit()
conn.close()