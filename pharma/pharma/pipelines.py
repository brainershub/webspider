# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

#from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_, not_, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
import datetime

from pharma.models import Items, create_items_table, db_connect
from pharma.features import clean_date

class PharmaPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates items table.
        """
        engine = db_connect()
        create_items_table(engine)
        Session = sessionmaker(bind=engine)

    # def open_spider(self, spider):
    #     session = self.Session()

    # def close_spider(self, spider):
        

    def process_item(self, item, spider):
        """
        Process the item and store to database.
        """
        if not item['content_text']:
            raise DropItem(f"No content_text found for {item['url']!r}")

        session = self.Session()
        # instance = session.query(Items).filter(or_(Items.title.like(item['title']), Items.url.like(item['url'])))
        instance = session.query(Items).filter(Items.url==item['url']).first()
        if instance:
            raise DropItem(f"Duplicate item found for: {item['url']!r}")
            # return instance

        if isinstance(item['content_date'], datetime.date):
            zelda_item = Items(**item)
        else:
            try:
                item['content_date'] = clean_date(item['content_date'])
                zelda_item = Items(**item)
            except:
                raise DropItem(f"No content_date: {item['content_date']!r}")

        # try:
        #     session.add(zelda_item)
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()
        
        session.add(zelda_item)
        session.commit()
        session.close()

        return item
    
    #OLD VERS
    # def open_spider(self, spider):
    #     hostname = '172.25.0.2'
    #     username = 'postgres'
    #     password = '123' # your password
    #     database = 'content'
    #     self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    #     self.cur = self.connection.cursor()

    # def close_spider(self, spider):
    #     self.cur.close()
    #     self.connection.close()

    # def process_item(self, item, spider):
    #     self.cur.execute("insert into content(title,author,text,content_date,url) values(%s,%s,%s,%s,%s)",(item['title'],item['author'],item['text'],item['content_date'],item['url']))
    #     self.connection.commit()
    #     return item

class NoTextPipeline():
    def __init__(self) -> None:
        pass

class DataBasePipeline():
    def __init__(self, db_set):
        self.database_settings = db_set

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_set = crawler.settings.get('DATABASE')
        )

    def open_spider(self, spider):
        self.engine = create_engine(URL(**self.database_settings))
        create_items_table(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        if not item['content_text']:
            raise DropItem(f"No content_text found for {item['url']!r}")

        instance = self.session.query(Items).filter(Items.url==item['url']).first()
        if instance:
            raise DropItem(f"Duplicate item found for: {item['url']!r}")
            # return instance

        if isinstance(item['content_date'], datetime.date):
            zelda_item = Items(**item)
        else:
            try:
                item['content_date'] = clean_date(item['content_date'])
                zelda_item = Items(**item)
            except:
                raise DropItem(f"No content_date: {item['content_date']!r}")#
        
        self.session.add(zelda_item)
        self.session.commit()

        return item
        