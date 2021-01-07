from dataclasses import dataclass


@dataclass
class Post:
    """Simple resource class """

    author_id: int
    title: str = ""
    body: str = ""

    @property
    def post(self):
        return self.__dict__