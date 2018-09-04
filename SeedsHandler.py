# coding=utf8

"""
    种子生成器
    author  : wangjiawei
    date    : 2018-08-30

    这个脚本里做两件事:

    1. 更新车系以及车系库
    2. 生产种子
    3. 提供种子导入的部分


    * 后期可以添加一个把有序种子变成无序的种子
"""

import random
import datetime
from copy import deepcopy
from BrandSeriseHandler import main_get_brands_serises
from utils import make_generator
from utils import make_list
from utils import dumps_json
from utils import write_2_file


serise_file = './DB/all_serise.csv'
city_list_file = './DB/city_list.csv'
seed_file = './DB/seeds_store.txt'
seed_url = 'https://www.guazi.com/{0}/dealrecord?tag_id={1}&date={2}00'
blank = '\t'

seed_demo = {
        'brand': '',
        'serise': '',
        'url': '',
        'check_city': '',
        'check_year': '',
        'check_month': '',
        'cookie': {},
        'cookie_status': 0,
    }

# 第一步就是更新品牌和车系的数据

def update_brands_serise():
    """
    自动的去更新品牌以及车系的数据
    :return:
    """
    main_get_brands_serises()
    return

# 第二步就是生产种子过程了

# 种子的格式为:

def seeds_maker():
    """
    开始fuck seeds了
    生成一个车型的全部请求的url,包含用不同的城市，以及不同的月份
    虽然结果都是展示的当前月份
    seed = {
        'brand': xxxx,
        'serise': xxxx,
        'url': xxxxx,
        'check_city': xxxx,
        'check_year': xxxx,
        'check_month': xxxx,
        'cookie': {},
        'cookie_status': 0,
    }
    """
    serise_list = make_generator(serise_file, blank=blank)
    for each in serise_list:
        construct_seed(each[2], each[1], each[-2])
    return

def construct_seed(serise_id, brand, serise):
    """这里是seed的装配厂"""
    #   首先确定年份和月份
    current_year = datetime.datetime.today().strftime("%Y")
    current_month = datetime.datetime.today().strftime("%m")
    #   城市集合以及年份集合
    city_list = make_list(city_list_file, index=1, blank=blank)
    year_list = [i for i in range(2000, int(current_year) + 1)]
    #   年份从大到小
    year_list.reverse()
    for year in year_list:
        #   载入月份
        if year != int(current_year):
            for m in [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]:
                city = random.choice(city_list)
                url = seed_url.format(city, serise_id, ''.join([str(year), str(random.choice(m))]))
                insert_seed_save(url, brand, serise, city, year, m)
        else:
            # 当前年份
            for m in range(1, int(current_month) + 1):
                city = random.choice(city_list)
                url = seed_url.format(city, serise_id, ''.join([str(year), str(m)]))
                insert_seed_save(url, brand, serise, city, year, m)
    return

def insert_seed_save(url, brand, serise, city, year, month):
    """注入seed以及保存"""
    seed = deepcopy(seed_demo)
    seed.update({'url': url,
                 'brand': brand,
                 'serise': serise,
                 'check_city': city,
                 'check_year': year,
                 'check_month': month,
                 })
    write_2_file(seed_file, dumps_json(seed))
    del seed
    return

#  生成一个生成器,来导入种子

def loads_seed_in_generator():
    """返回一个生成器，导入种子
    上层在调用的时候
    通过 next()函数,一次一次调用
    """
    return make_generator(seed_file, '')