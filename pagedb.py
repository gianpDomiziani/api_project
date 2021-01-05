import sqlite3

# init a db session
conn = sqlite3.connect('page.db')
# create a curso object 
cursor = conn.cursor()
# use its execute method for performing the following SQL query
cursor.execute(""" CREATE TABLE pages
                   (id integer, title text, header text, author text, body text) """)
# save the change and close the session.
conn.commit()
conn.close()