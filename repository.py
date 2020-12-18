import abc
from models.page import ServePages

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, page: dict):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int, ServePages) -> dict:
        raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, page):
        self.session.add(page)
    
    def get(self, id: int, ServePages) -> dict:
        return self.session.query(ServePages.pages).filter_by(id).one()
    
    def list(self):
        return self.session.query(ServePages.pages).all()


