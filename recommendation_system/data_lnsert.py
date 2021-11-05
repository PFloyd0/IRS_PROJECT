# -*- coding: utf-8 -*-

import pandas as pd
import pymysql


class BookSqlTools:
    # 链接MYSQL数据库
    # 读取出来转化成pandas的dataframe格式

    def LinkMysql(self, sql):
        print('正在连接====')
        try:
            connection = pymysql.connect(user="root",
                                         password="19990520",
                                         port=3306,
                                         host="127.0.0.1",  # 本地数据库  等同于localhost
                                         db="Book",
                                         charset="utf8")
            cur = connection.cursor()

        except Exception as e:
            print("Mysql link fail：%s" % e)
        try:
            cur.execute(sql)

        except Exception as e:
            print("dont do execute sql")
        try:
            result1 = cur.fetchall()
            title1 = [i[0] for i in cur.description]
            Main = pd.DataFrame(result1)
            Main.columns = title1

        except Exception as e:
            print(" select Mysql error：{}".format(e))
        return Main

    # 数据库中的表插入数据
    def UpdateMysqlTable(self, data, sql_qingli, sql_insert):
        try:
            connection = pymysql.connect(user="root",
                                         password="19990520",
                                         port=3306,
                                         host="127.0.0.1",  # 本地数据库  等同于localhost
                                         db="Book",
                                         charset="utf8")
            cursor = connection.cursor()

        except Exception as e:
            print("Mysql link fail：%s" % e)
        try:
            cursor.execute(sql_qingli)
        except:
            print("dont do created table sql")
        try:
            for i in data.index:
                x = list(pd.Series(data.iloc[i,].astype(str)))
                sql = sql_insert.format(tuple(x)).encode(encoding='utf-8')
                print(sql)
                try:
                    cursor.execute(sql)
                except Exception as e:
                    print("Mysql insert fail%s" % e)
        except Exception as e:
            connection.rollback()
            print("Mysql insert fail%s" % e)
        connection.commit()
        cursor.close()
        connection.close()


connection = pymysql.connect(user="root",
                             password="19990520",
                             port=3306,
                             host="127.0.0.1",  # 本地数据库  等同于localhost
                             charset="utf8")

cur = connection.cursor()
cur.execute('DROP DATABASE if exists Book')
cur.execute('CREATE DATABASE if not exists Book')
connection.commit()
cur.close()
# 创建购物车表

connection = pymysql.connect(user="root",
                             password="19990520",
                             port=3306,
                             db="Book",
                             host="127.0.0.1",
                             charset="utf8")

cur = connection.cursor()
createCartSql = '''CREATE TABLE Cart
               (Id                   int primary key not null auto_increment,
               UserID                 VARCHAR(100)   ,
                BookID                VARCHAR(100));'''
cur.execute(createCartSql)
connection.commit()
cur.close()
connection.close()

BookInfoInsert = BookSqlTools()



# --------------------------------------------------------------------------
# 读取本地的book1-100k.csv文件  在数据库中建一个Books表   将book.csv内容插入到数据库中
# --------------------------------------------------------------------------

path = '../data/book1-100k.csv'
Book = pd.read_csv(path, sep=",", encoding="ISO-8859-1", error_bad_lines=False)

createBooksSql = ''' CREATE TABLE Books
               (Id                   INT PRIMARY KEY,
                Name                VARCHAR(999) ,
                RatingDist1         VARCHAR(999) ,
                pagesNumber               INT ,
                RatingDist4          VARCHAR(999) ,
                RatingDistTotal                VARCHAR(999) ,
                PublishMonth                   INT ,
                PublishDay                   INT ,
                Publisher                   VARCHAR(999) ,
                CountsOfReview          INT ,
                PublishYear                INT ,
                Language                   VARCHAR(999) ,
                Authors                   VARCHAR(999) ,
                Rating                   FLOAT,
                RatingDist2             VARCHAR(999) ,
                RatingDist5             VARCHAR(999) ,
                ISBN                    VARCHAR(999) ,
                RatingDist3             VARCHAR(999));'''

BooksSql_insert = 'insert into Books (Id,Name,RatingDist1,pagesNumber,RatingDist4,RatingDistTotal,PublishMonth,PublishDay,Publisher,CountsOfReview,PublishYear,Language,Authors,Rating,RatingDist2,RatingDist5,ISBN,RatingDist3) values {}'

BookInfoInsert.UpdateMysqlTable(Book, createBooksSql, BooksSql_insert)
del Book

# --------------------------------------------------------------------------
# 读取本地的ratings_csv文件  在数据库中建一个Bookrating表   将bookrating.csv内容插入到数据库中
# --------------------------------------------------------------------------

path = '../data/ratings_csv.csv'
Rating = pd.read_csv(path, sep=",", encoding="ISO-8859-1", error_bad_lines=False)

createBookratingSql = '''CREATE TABLE Bookrating
               (Id                   int primary key not null auto_increment,
               User_Id                INT ,
                Name                INT,
                Rating                INT);'''

BookratingSql_insert = 'insert into Bookrating (User_Id, Name, Rating) values {}'

BookInfoInsert.UpdateMysqlTable(Rating, createBookratingSql, BookratingSql_insert)
del Rating


