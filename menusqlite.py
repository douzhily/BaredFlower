# -*- coding: UTF-8 -*-

import sqlite3

def db_init(conn, cur):
	cur.execute('CREATE TABLE IF NOT EXISTS dishes (id integer PRIMARY KEY autoincrement, name text NOT NULL, cuisine integer, memo text, status boolean);')
	cur.execute('CREATE TABLE IF NOT EXISTS cuisines (id integer PRIMARY KEY autoincrement, name text NOT NULL, memo text);')
	
	conn.commit()

def db_default_dishes(conn, cur):
	cur.execute('INSERT INTO dishes (name, cuisine, status) VALUES (\'Salad\', 1, 1);')
	cur.execute('INSERT INTO dishes (name, cuisine, status) VALUES (\'Chicken\', 1, 1);')
	cur.execute('INSERT INTO dishes (name, cuisine, status) VALUES (\'Humburger\', 1, 1);')
	conn.commit()
	cur.execute('SELECT * FROM dishes WHERE status = 1;')
	dishes_list = cur.fetchall()
	print dishes_list

def db_default_cuisine(conn, cur):
	cur.execute('INSERT INTO cuisines (name) VALUES (\'Western\');')
	cur.execute('INSERT INTO cuisines (name) VALUES (\'东北菜\');')
	cur.execute('INSERT INTO cuisines (name) VALUES (\'川菜\');')
	cur.execute('INSERT INTO cuisines (name) VALUES (\'湖北菜\');')
	conn.commit()

def select_all_dishes(conn, cur, cuisine_id = 0):
	if cuisine_id == 0:
		cur.execute('SELECT name FROM dishes WHERE status = 1;')
		dishes_list = cur.fetchall()
	else:
		cur.execute('SELECT name FROM dishes WHERE status = 1 AND cuisine = \'%s\';' % cuisine_id)
		dishes_list = cur.fetchall()
	format_dish_list = []
	for dish_1 in dishes_list:
		dish = dish_1[0].encode('utf-8')
		format_dish_list.append(dish)
	return format_dish_list

def select_all_cuisines(conn, cur):
	cur.execute('SELECT id, name FROM cuisines ORDER BY id ASC;')
	cuisines_list = cur.fetchall()
	format_cuisines_list = {}
	for cuisine_1 in cuisines_list:
		cuisine_id = str(cuisine_1[0])
		cuisine = cuisine_1[1].encode('utf-8')
		format_cuisines_list[cuisine_id] = cuisine
	return format_cuisines_list

def dish_info(conn, cur, search_info):
	cur.execute('SELECT dishes.id, dishes.name, cuisines.name, dishes.memo FROM dishes INNER JOIN cuisines ON dishes.cuisine = cuisines.id WHERE dishes.name = \'%s\';' % search_info)
	#print cur.fetchall()
	dish_info = cur.fetchall()[0]
	dish_id = dish_info[0]
	dish_name = dish_info[1].encode('utf-8')
	dish_cui = dish_info[2].encode('utf-8')
	if dish_info[3]:
		dish_memo = dish_info[3].encode('utf-8')
		dish_format_info = [dish_id, dish_name, dish_cui, dish_memo]
	else:
		dish_format_info = [dish_id, dish_name, dish_cui]
	return dish_format_info








