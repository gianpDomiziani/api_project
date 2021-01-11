/* There is a one-to-many relation between the two tables (each user can have multiple posts). 
User is the parent table, post is the child table.
user.id is the parent key, post.author_id is the child key. If a primary_key is deleted the correspondent 
child_key is set to NULL. */
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

PRAGMA foreign_keys = ON;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
  );

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  edit INTEGER,
  FOREIGN KEY (author_id) REFERENCES user(id)
    ON DELETE SET DEFAULT
  );
