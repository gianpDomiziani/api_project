import pytest
import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)

from app.models import post_model

post0 = post_model.Post(id_=0, author_id=0, author='user1', title='title1', body='body1.').post
post1 = post_model.Post(id_=1, author_id=1, author='user2', title='title2', body='body2').post


class TestModel:

    @staticmethod
    def test_post():
        assert post0['id_'] == 0
        assert post1['id_'] == 1
        assert isinstance(post1, dict)
        assert len(post0.keys()) == 6
        assert len(post1.keys()) == 6
        assert type(post1['body']) == str

    @staticmethod
    def test_posts_are_unique_by_id():
        post_a = post_model.Post(id_=12, title='Luna')
        post_b = post_model.Post(id_=13, title='Luna')
        assert post_a != post_b
