from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, ForeignKey
)

from sqlalchemy.orm import mapper, relationship

import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)

from models import page_model

metadata = MetaData()

pages = Table(
    'pages', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('pageid', Integer),
    Column('title', String(255)),
    Column('header', String()),
    Column('author', String()),
    Column('body', String()),
)

def start_mapper():
    pages_mapper = mapper(page_model.Page, pages)
