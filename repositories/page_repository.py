import abc
import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)

from models.page_model import Page

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, page: dict):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int, ServePages) -> dict:
        raise NotImplementedError

class FakeRepository(AbstractRepository):

    def __init__(self, pages):
        self._pages = set(pages)
    
    def add(self, page):
        self._pages.add(page)

    def get(self, id):
        return next(b for b in self._pages if b.pageid == id)
    
    def list(self):
        return list(self._pages)
    

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, page):
        self.session.add(page)
    
    def get(self, id: int, Page) -> dict:
        return self.session.query(Page).filter_by(id).one()
    
    def list(self):
        return self.session.query(Page).all()


