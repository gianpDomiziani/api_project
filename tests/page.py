

class Page:

    def __init__(self, id=None, title="", header="", author="", body=""):

        self._id = id
        self._title = title
        self._header = header
        self._author = author
        self._body = body
        self._page = {"id": self._id, "title": self._title, "header": self._header, 
                      "author": self._author, "body": self._body}
        


class ServePages:

    def __init__(self):
        self._pages = dict()
    
    def charge(self, pgs: dict)-> None:
        self._pages[pgs['id']] = pgs
        

    def get(self, id: int):

        try:
            return self._pages[id]
        except KeyError:
            return None
    
    def delete(self, id: int):
        
        try:
            _ = self._pages.pop(id)
            return True
        except KeyError as e:
            print(e)
            return False

    def modify(self, id: int, field: str, content=''):

        try:
            self._pages[id][field] = content
            return True
        except KeyError as e:
            print(e)
            return False


    

        
        



