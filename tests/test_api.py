import pytest
import uuid
import requests

def random_suffix():
    return uuid.uuid4().hex[:6]

def random_title(title=''):
    return f'title_{title}_{random_suffix()}'

def random_author(author=''):
    return f'author_{author}_{random_suffix()}'

def random_header(header=''):
    return f'header_{header}_{random_suffix()}'

def random_body():
    return f'body_{random_suffix()}'

class TestApi:

    @staticmethod
    def test_
