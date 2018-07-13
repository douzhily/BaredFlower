# -*- coding: UTF-8 -*-

import settings
import menusqlite
import sqlite3
import choice
import utils
import init

print '*******  Welcome to Doudou Kitchen v 2.0!  *******\n********** 新版本特性 **********\n* 不用再拖拽文件啦'

conn = sqlite3.connect('random_menu.db')
cur = conn.cursor()

init.init(conn, cur)

while 1:
	print '* 按菜系选菜 --- 输入 【c】\n* 进入设置 ---- 输入【menu】\n* 退出 ---- 输入【q】.'

	num = raw_input('* 随机出菜，请输入菜的个数：')
	op = utils.quit_or_not(num)
	if op == 1:
		cur.close()
		conn.close()
		print 'Bye.'
		break
	else:
		if num in ('menu', 'MENU'):
			settings.options(conn, cur)
		elif num in ('c', 'C'):
			choice.dish_choice_with_cuisine(conn, cur)
		else:
			choice.dish_choice(num, conn, cur)





