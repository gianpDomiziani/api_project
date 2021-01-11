from dataclasses import dataclass

@dataclass
class User:

    username: str
    password: str

    @property
    def get_user(self):
        return self.__dict__
