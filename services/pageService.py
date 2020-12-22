from dataclasses import dataclass

@dataclass
class ServePages:
    """ServePages is a service layer interface (controller) for applying our application logic to the Pages resources. 
    It follows the REST architectural style, however remaining totally independent from the HTTP protocol. """

    @property
    def pages(self):
        return self.__dict__

    @property
    def totPages(self) -> int:
        return len(self.pages.keys())

    
    # POST
    def charge(self, pgs: dict) -> None:
        self.pages[pgs['id']] = pgs  # save a page by its ID

    # GET
    def get(self, id: int):

        try:
            return self.pages[id]
        except KeyError:
            return None

    # DELETE
    def delete(self, id: int):

        try:
            _ = self.pages.pop(id)
            return True
        except KeyError as e:
            print(e)
            return False

    # PUT: even if only the given field is modified, while in a PUT the entire resource is replaced by the new one.
    def modify(self, id: int, field: str, content=''):

        try:
            self.pages[id][field] = content
            return True
        except KeyError as e:
            print(e)
            return False