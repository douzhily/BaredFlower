# -*- coding: UTF-8 -*-

import re
import os
import menusqlite
import sqlite3
import utils


def options(conn, cur):
	print '**************  设置  **************'
	option = raw_input('* 添加菜名 -------- 输入 【1】\n* 搜索菜名 -------- 输入 【2】\n* 查看整个菜单 ---- 输入 【3】\n* 导入txt文件 ---- 输入【4】')
	if option == '1':
		add_dish(conn, cur)
	elif option == '2':
		search_dish(conn, cur)
	elif option == '3':
		show_dishes_list(conn, cur)
	elif option == '4':
		imp_dishes_list(conn, cur)


def add_dish(conn, cur):
	while 1:
		new_dish = raw_input('添加新菜名：')
		if len(new_dish) == 0:
			print '不要直接回车哦'
		else:
			break
	exist_dishes = menusqlite.select_all_dishes(conn, cur)
	if new_dish in exist_dishes:
		print '菜单中已存在【' + new_dish + '】。' + '\n'
	else:
		#打印所有菜系名字和id
		id_list = utils.show_cuisines_list(conn, cur)
		while 1: 
			cuisine_info = raw_input('请输入需要添加的菜系 id：').strip()
			if len(cuisine_info) == 0:
				cur.execute('INSERT INTO dishes (name, status) VALUES (\'%s\', 1);' % new_dish)
				conn.commit()
				break
			elif cuisine_info in ('q', 'Q'):
				cur.execute('INSERT INTO dishes (name, status) VALUES (\'%s\', 1);' % new_dish)
				conn.commit()
				break
			else:
				cur.execute('SELECT id FROM cuisines;')
				cuisine_num = cur.fetchone()
				if cuisine_info in id_list:
					cur.execute('INSERT INTO dishes (name, cuisine, status) VALUES (\'%s\', \'%s\', 1);' % (new_dish, cuisine_info))
					conn.commit()
					break
				else:
					print '------- 请参考上方id列表 ---------'
		memo = raw_input('【' + new_dish + '】已添加至菜单，如果需要添加备注（外卖信息，你懂得），请输入：\n').strip()
		if len(memo) == 0:
			print '以后想添加备注信息也可以的'
		else:
			cur.execute('UPDATE dishes SET memo = \'%s\' WHERE name = ' % memo + '\'%s\';' % new_dish)
			conn.commit()

def search_dish(conn, cur):
	while 1:
		search_info = raw_input('请输入搜索关键词：')
		if len(search_info) == 0:
			print '不要直接回车哦'
		else:
			status = utils.quit_or_not(search_info)
			if status == 1:
				break
			else:
				exist_dishes = menusqlite.select_all_dishes(conn, cur)
				exist_dishes_decode = []
				for dish in exist_dishes:
					dish_decode = dish.decode('utf-8')
					exist_dishes_decode.append(dish_decode)
				search_info_decode = search_info.decode('utf-8')
				if search_info_decode in exist_dishes_decode:
					print '菜单中已存在【' + search_info + '】。\n'
					dish_info = menusqlite.dish_info(conn, cur, search_info)
					if len(dish_info) == 3:
						print '【' + dish_info[1] + '】的id是【' + str(dish_info[0]) + '】，菜系是【' + dish_info[2] + '】。'
					else:
						print '【' + dish_info[1] + '】的id是【' + str(dish_info[0]) + '】，菜系是【' + dish_info[2] + '】， 备注是【' + dish_info[3] + '】。'
					break
				else:
					print '我们尝试进行模糊搜索，结果如下：'
					for dish in exist_dishes:
						if search_info in dish:
							print '-' + dish			
					add_op = raw_input('菜单中还没有【' + search_info + '】哦，需要添加的话输入【Y】:')
					if add_op in ('y', 'Y'):
						cur.execute('INSERT INTO dishes (name, status) VALUES (\'%s\', 1);' % search_info)
						conn.commit()
						print '【' + search_info + '】已添加至菜单。\n'
					break
def show_dishes_list(conn, cur):
#打印所有菜名
	print '\n************  所有菜名  ************'
	exist_dishes = menusqlite.select_all_dishes(conn, cur)
	for dish in exist_dishes:
		print '- ' + dish
	print ' '



def imp_dishes_list(conn, cur):
#导入菜单
	while 1:
		status = 1
		dishes_ad = raw_input('把菜单文件拽到这里,或按【Q】退出：').strip()
		if os.path.isfile(dishes_ad):
			dishes_file = dishes_ad
			break
		elif dishes_ad in ('q', 'Q'):
			status = 0
			break
		else:
			print '请拖拽文件到此处：'
	while status == 1:
		d_file = open(dishes_file, 'r+')
		dish_list = d_file.read()
		if dish_list.strip() == '':
			print '文件是空的，请不要添加空文件。'
			break
		else:
			exist_dishes = menusqlite.select_all_dishes(conn, cur)
			new_dishes = re.split(',|\n| |，|、', dish_list)
			count = 0
			for dish in new_dishes:
				if dish not in exist_dishes:
					cur.execute('INSERT INTO dishes (name, status) VALUES (\'%s\', 1);' % dish)
					conn.commit()
					count = count + 1
					print '【' + dish + '】已添加至菜单。'
			print '本次导入共添加 %d 个菜。' % count
			break


