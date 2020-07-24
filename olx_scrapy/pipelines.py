# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class OlxScrapyPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("olx_database.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS olx_tb""")
        self.curr.execute("""create table olx_tb(
                        title text,
                        price text,
                        city text,
                        date text
                        )""")


    def process_item(self, item, spider):
        self.store_db(item)

        return item

    def store_db(self,item):
        self.curr.execute("""insert into olx_tb values(?,?,?,?)""",(
            item['title'][0],
            item['price'][0],
            item['city'],
            item['date']
        ))
        self.conn.commit()
