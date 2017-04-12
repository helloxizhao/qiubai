# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import  json
import  MySQLdb
import  MySQLdb.cursors
from twisted.enterprise import adbapi
class QiubaiPipeline(object):
    def open_spider(self,spider):
        self.file = codecs.open('qiubai.jl','wb',encoding='utf-8')
    def process_item(self,item,spider):
        line = json.dumps(dict(item),ensure_ascii=False)
        self.file.write(line+'\n')
        return item
    def close_spider(self,spider):
        self.file.close()
class MysqlQuibaiPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
             host = settings['MYSQL_HOST'],
             db = settings['MYSQL_DBNAME'],
             user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb',**dbargs)
        return cls(dbpool)
    def process_item(self,item,spider):
        res = self.dbpool.runInteraction(self.insert_into_table,item)
        #print item['content']
        return item
    def insert_into_table(self,conn,item):
        #print item['content']
        conn.execute('insert into qiubai values(%s)',
            (item['content'].encode('utf-8'),
        ))
