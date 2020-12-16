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
    
    def build_json_response(self, http_status: int, api_method: str) -> str:

        json_body = json.dumps(self._page["body"], indent=4, sort_keys=False)
        ans = {
            'body': json_body,
            'http_status_code': http_status,
            'API': api_method
        }
        ans_json = json.dumps(ans, indent=4, sort_keys=False)
        return ans_json



if __name__ == '__main__':

    pgs = Page(id=1, title='Mars', header='Can Mars hospit life?', author='Pino', body='Yes.')
    j = pgs.build_json_response(http_status=200, api_method='getPage')
    print(j)


