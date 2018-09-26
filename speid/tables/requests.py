from sqlalchemy import Column, Enum, JSON, String

from speid import db

from . import cols
from .types import HttpRequestMethod


requests = db.Table(
    'requests', db.metadata,
    cols.id('RQ'), cols.created_at(),
    Column('method', Enum(HttpRequestMethod, name='http_request_method'),
           nullable=False),
    Column('path', String(256), nullable=False),
    Column('query_string', String(1024)),
    Column('ip_address', String(45), nullable=False),
    Column('headers', JSON),
    Column('body', String)
)