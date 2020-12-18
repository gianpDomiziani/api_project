import abc
from models.page import Page

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, page: Page):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Page:
        raise NotImplementedError

class SQLAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, page: Page):
        self.session.add(page)
    
    def get(self, id: int) -> Page:
        return self.session.query()


