import json
from flask import Response 

class Page:

    def __init__(self, id=None, title="", header="", author="", body=""):

        self._id = id
        self._title = title
        self._header = header
        self._author = author
        self._body = body
        self._page = {"id": self._id, "title": self._title, "header": self._header, 
                      "author": self._author, "body": self._body}

