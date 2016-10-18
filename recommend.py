# -*- coding:utf-8 -*-
from random import choice
import MySQLdb


def recommend(user):
    try:
        # 连接数据库
        DB = MySQLdb.connect("localhost", "root", "qq920534583", "recommend")
        # 获取游标
        c = DB.cursor()

        # 下面代码实现从数据库中得到用户user喜欢的番剧编号，以便避免重复
        love = []
        # sql语句
        sql = "SELECT anime_id FROM user_anime WHERE user_id=%s;"
        c.execute(sql, str(user))
        # 得到结果集，接收全部的返回结果行
        results = c.fetchall()
        for line in results:
            love.append(line[0])

        # 下面代码实现得到用户喜欢的top3类型
        sql = '''
        select style_id from
            (select user_id,style_id from
            (select user_id,anime_id as id from user_anime where user_id=%s) as s
            natural join anime natural join
            (select anime_id as id,style_id from anime_style) as n
             )as temp group by style_id order by count(user_id) desc limit 3;
             '''
        c.execute(sql, str(user))
        results = c.fetchall()
        lis = []
        anime = {}
        for line in results:
            lis.append(line[0])

        # 从番剧信息的数据库anime_style中得到top3各个类别的所有番剧并存到anime字典中
        for i in lis:
            sql = "SELECT anime_id FROM anime_style WHERE style_id={};".format(i)
            c.execute(sql)
            results = c.fetchall()
            anime_lis = []
            for result in results:
                anime_lis.append(result[0])
            # 类型为key，值为存放番剧数据的列表
            anime[str(i)] = anime_lis
        # 建立三个类别番组的set(集合），并取交集，即得到同时具有三个类型标签的番剧
        s = set(anime[str(lis[0])]) & set(anime[str(lis[1])]) & set(anime[str(lis[2])])

        # 建立用户喜欢番剧的集合
        loveset = set(love)

        # 如果系统得到的所有番剧用户都已看过，即loveset>s，就从TOP1类型即最喜欢的类型里挑选一个
        if loveset > s:
            s = set(anime[str(list[0])])

        # 把集合转换成列表提供给随机函数使用
        set_lis = []
        for i in s:
            set_lis.append(i)

        # 从结果中随机挑选
        recommendation = choice(set_lis)

        # 直到挑选到用户没看过的，（上文有个if判断，所以这里set_lis>love，不会陷入死循环，）
        while recommendation in love:
            recommendation = choice(set_lis)
        dic = {}

        # 得到番剧的相关信息
        sql = "SELECT name,brief FROM anime WHERE id={};".format(recommendation)
        c.execute(sql)
        results = c.fetchall()
        dic['name'] = results[0][0]
        dic['brief'] = results[0][1]
    finally:
        # 关闭指针和连接
        c.close()
        DB.close()
        return dic

