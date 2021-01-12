from dataclasses import dataclass
import datetime

@dataclass
class Post:
    """Simple resource class """

    id_: int = 0
    author_id: int = 0
    author: str = ""
    title: str = ""
    body: str = ""
    created: str = ""

    @property
    def post(self):
        return self.__dict__
    
    @classmethod
    def new_post(cls, author_id, title, body):
        """ a simply class method for creating a new post to be insert.
        Once the new post is created the post_repository will return a complete post object. """

        return {"author_id": author_id, "title": title, "body": body}