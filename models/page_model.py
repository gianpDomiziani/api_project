from dataclasses import dataclass


@dataclass
class Page:
    """Simple resource class """

    pageid: int
    title: str = ""
    header: str = ""
    author: str = ""
    body: str = ""

    @property
    def page(self):
        return self.__dict__