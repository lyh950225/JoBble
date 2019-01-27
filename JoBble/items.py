# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from JoBble.utils.common import date_convert
import scrapy
from JoBble.utils.common import *
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def get_nums(value):
    match_re = re.match(".*?(\d+).*?", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobbleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    creat_time = scrapy.Field(
        input_processor=MapCompose(TakeFirst(), deal_with_time, date_convert)
    )
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    faves_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tag_list = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    contens = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                            insert into jobbole (title, url, create_time, faves_nums)
                            VALUES (%s, %s, %s, %s)
                            """
        params = (self['title'], self['url'], self['create_time'], self['faves_nums'])
        return insert_sql, params



