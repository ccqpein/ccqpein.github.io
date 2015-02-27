#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time

#参数传递
script, filename = sys.argv 

if __name__ == "__main__":

	#如果输入了.md则删除掉
	filename = re.sub(r'\.md', '', filename)

	#读取文件，为防止最后没有换行，和下面冲突，最后添加一个换行
	s = open(filename+'.md','r').readlines()
	s[-1] = s[-1] + '\n'
	ss = []

	#定义头文件的变量
	title = ['"','','"', '\n']

	creat_date = time.ctime(os.path.getctime(filename+'.md')).split()
	modify_date = time.ctime(os.path.getmtime(filename+'.md'))
	yearTable = {'Feb':2, }

	#定义头文件，空格不可省
	headd = ['---\n', 'layout:     post\n', 'title:      ', '', 'subtitle:   ', '', 
			'date:       ', '', 'author:     "ccQ"\n', 'header-img: ', '\n', '---\n']

	#开始替换样式，从多＃替换到少＃
	for strs in s:
		if re.match(r'(\#\#)', strs):
			strs = re.sub(r'(\#\#){1}', '<h2 class="section-heading">', strs)
			strs = re.sub(r'\n$', '</h2>\n', strs)
			ss += strs
			continue

		if re.match(r'(\#)', strs):
			strs = re.sub(r'(\#){1}', '', strs)
			title[1] = re.sub(r'\n$', '', strs)
			strs = ''
			ss += strs
			continue
		'''
		if strs == '\n':
			ss += strs
			continue
		else:
			strs = re.sub(r'\n$', '</p>\n', strs)
			strs = '<p>' + strs
			ss += strs
			continue
		'''
		
	ss = ''.join(ss)

	#头文件变量定义，加入正文
	headd[3] = ''.join(title)
	#副标题不好看，去掉了
	#headd[5] = '"' + modify_date + '最后修改' + '"\n'
	headd[7] = creat_date[4] +'-' +str(yearTable['Feb']) +'-' +creat_date[2] +' ' +creat_date[3] +'\n'

	headline = ''.join(headd)

	ss = headline + ss 

	#写出
	open(headd[7][:9] + '-' + filename + '.md', 'w').write(ss)
	
	#print()