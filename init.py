# -*- coding: UTF-8 -*-

import sqlite3
import menusqlite

def init(conn, cur):
	menusqlite.db_init(conn, cur)
	dishes_init(conn, cur)
	cuisines_init(conn, cur)

def dishes_init(conn, cur):
	cur.execute('SELECT COUNT(*) FROM dishes WHERE status = 1;')
	active_dish_num = cur.fetchone()
	#如果没有数据，添加默认数据
	if active_dish_num[0] == 0:
		menusqlite.db_default_dishes(conn, cur)
		print 'We added 3 default dishes for you.'

def cuisines_init(conn, cur):
	cur.execute('SELECT COUNT(*) FROM cuisines;')
	cuisine_num = cur.fetchone()
	if cuisine_num[0] == 0:
		menusqlite.db_default_cuisine(conn, cur)
		print 'We added 1 default cuisine for you.'
