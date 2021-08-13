from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
import os
from datetime import datetime
import json as js

from pharma import settings
# from pharma.features import clean_date
from pharma.nlp.NLP_insights import NLP_module
from pharma.nlp.Word_counter import genarate_word_count

DeclarativeBase = declarative_base()

def db_connect() -> Engine:
    """
    Creates database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    # return create_engine(SQLALCHEMY_DATABASE_URI)
    return create_engine(URL(**settings.DATABASE))

def create_items_table(engine: Engine):
    """
    Create the Items table
    """
    DeclarativeBase.metadata.create_all(engine, checkfirst=True)

class Items(DeclarativeBase):
    """
    Defines the items model
    """

    # __tablename__ = "content"
    # __tablename__ = "content_crawled_test_3"
    __tablename__ = os.environ['TABLE_CONTENT']

    id = Column("id", Integer, primary_key=True)
    title = Column('title', Text)
    author = Column('author', Text)
    content_text = Column('text', Text)
    content_date = Column('content_date', DateTime)
    url = Column('url', Text)
    url_base = Column('url_base', Text)
    summary = Column('summary', Text)
    wordcount = Column('wordcount', Text)
    crawling_date = Column('crawling_date', DateTime, default=datetime.utcnow)
    labels = Column('labels', Text)
    
    def __init__(self, title, author, content_text, content_date, url, url_base, labels):

        self.url = url
        self.url_base = url_base

        
        self.content_date = content_date
        # except:
        #     self.content_date = content_date

        self.title = title
        self.author = author

        text_cleaned = " ".join(content_text.split())
        self.content_text = text_cleaned

        if isinstance(text_cleaned, str):
            self.wordcount = js.dumps(genarate_word_count(text_cleaned))
            try:
                nlp_obj = NLP_module(text_cleaned)
                self.summary = nlp_obj.get_summary()
            except:
                self.summary = 'FAILED TO BUILD SUMMARY'
        else:
            self.wordcount = 'TEXT IS NOT A STRING' 
            self.summary = 'TEXT IS NOT A STRING OR FAILED TO BUILD SUMMARY'
        
        self.labels = labels