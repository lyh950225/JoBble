import hashlib
import datetime
import re

def get_ma5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def date_convert(value):
    try:
        create_time = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_time = datetime.datetime.now().date()
    return create_time


def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


def deal_with_time(value):
    creat_time = value[0].strip().replace("·", "").strip()
    return creat_time


def return_value(value):
    return value


if __name__ == '__main__':

    print()
