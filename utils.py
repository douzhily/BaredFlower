# -*- coding: UTF-8 -*-

import random 
import menusqlite
import sqlite3
import init

def count_of_active_dish(conn, cur, cuisine_id = 0):
#返回有多少 active 的 dish	
	if cuisine_id == 0:
		cur.execute('SELECT COUNT(*) FROM dishes WHERE status = 1;')
		active_dish_num = cur.fetchone()
		print 'Now you have %s dishes.' % active_dish_num
		return active_dish_num[0]
	else:
		cur.execute('SELECT COUNT(*) FROM dishes WHERE status = 1 AND cuisine = \'%s\';' % cuisine_id)
		active_dish_num = cur.fetchone()
		print 'Now you have %s dishes in this cuisine' % active_dish_num
		return active_dish_num[0]

def count_of_cuisines(conn, cur):
#返回菜系数目
	cur.execute('SELECT COUNT(*) FROM cuisines;')
	cuisine_num = cur.fetchone()
	print 'Now you have %s cuisines' % cuisine_num
	return cuisine_num[0]

def show_cuisines_list(conn, cur):
#打印菜系列表，并返回菜系 id 的 Array
	print '\n************  所有菜系  ************'
	ids = []
	exist_cuisines = menusqlite.select_all_cuisines(conn, cur)
	for cuisine in exist_cuisines:
		print '- ' + cuisine + ' ' + exist_cuisines[cuisine]
		ids.append(cuisine)
	print ' '
	return ids

def quit_or_not(op):
	if op in ('q', 'Q'):
		return 1
	else:
		return 0