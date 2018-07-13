# -*- coding: UTF-8 -*-

import random 
import menusqlite
import sqlite3
import utils


def dish_choice(num, conn, cur, cuisine_id = 0):
	if utils.quit_or_not(num) == 1:
		return 0
	else:
		try:
			num = int(num)
		except ValueError:
			print '-------- 请输入整数 ---------'
			return 1
		else:
			if num <= 0:
				print '-------- 请输入大于0的整数 ---------'
				return 1
			else:
				#获取当前dishes表条数
				active_dish_num = utils.count_of_active_dish(conn, cur, cuisine_id)			

				#把所有dishes存到一个数组里
				today_list = menusqlite.select_all_dishes(conn, cur, cuisine_id)			

				if num < active_dish_num:
					today_rec = random.sample(today_list, num)
					print '\n**********  今日推荐菜谱  **********'
					for dish in today_rec:
						print '- ' + dish
				elif num == active_dish_num:
					print '\n**********  今日推荐菜谱  **********'
					for dish in today_list:
						print '- ' + dish
					print '菜谱库里只有这些菜了，你可以进入menu根据提示添加菜式'
				else:
					print '别逗我！要这么多？请先丰富您的菜谱库（输入menu根据提示添加）'
				print ' '
				return 0

def dish_choice_with_cuisine(conn, cur):
	cuisine_ids = utils.show_cuisines_list(conn, cur)
	while 1:
		target_id = raw_input('输入今天想吃的菜系id吧：').strip()
		if target_id in ('q', 'Q'):
			break
		elif target_id in cuisine_ids:
			target_id = int(target_id)
			num = raw_input('* 随机出菜，请输入菜的个数：')
			while 1:
				status = dish_choice(num, conn, cur)
				if status == 0:
					break
			break
		else:
			print '------- 请参考上方id列表 ---------'

