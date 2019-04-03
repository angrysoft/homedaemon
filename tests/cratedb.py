#!/usr/bin/python3

# import mysql.connector as mariadb
import MySQLdb
import json



def info(msg):
    print('>>  {}'.format(msg))


def create_db(adm, admpasswd, dbuser, dbpasswd, dbname):
    info('Crete DB: {}'.format(dbname))
    adm_conn = MySQLdb.connect(user=adm, password=admpasswd)
    adm_cur = adm_conn.cursor()
    adm_cur.execute("DROP USER IF EXISTS %s@localhost", (dbuser,))
    adm_cur.execute("CREATE USER %s@localhost IDENTIFIED BY %s", (dbuser, dbpasswd))
    adm_cur.execute("DROP DATABASE IF EXISTS {}".format(dbname))
    adm_cur.execute('''CREATE DATABASE {}
                       CHARACTER SET = "utf8"
                       COLLATE = "utf8_general_ci"'''.format(dbname))
    adm_cur.execute("GRANT ALL PRIVILEGES ON {}.* TO '{}'@'localhost'".format(dbname, dbuser))
    adm_cur.execute("FLUSH PRIVILEGES")
    adm_conn.commit()
    adm_conn.close()


if __name__ == '__main__':
    config = dict()
    admin = dict()
    with open('../files/angryhome.json', 'r') as jconf:
        config = json.load(jconf)
    with open('admin.json', 'r') as jadmin:
        admin = json.load(jadmin)

    create_db('root', admin.get('password'),
              config.get('user_db'), config.get('password_db'),
              config.get('name_db'))
