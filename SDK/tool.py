#! /usr/bin/env python
# -*- coding:utf-8 -*-
def WriteAllText(path,text):
	'''覆盖式写入文件'''
	pass
def AppendAllText(path,text):
	'''向文件中追加'''
	pass 
def ReadAllLine(path):
	'''返回一个list，每个value对应文件的每一行'''
	return 'list'
def ShareData(key,value):
	'''设置一个共享数据'''
	return 'ifsuccess'
def GetShareData(key):
	'''获取一个共享数据'''
	return 'value'
def ChangeShareData(key,value):
	'''修改共享数据'''
	return 'ifsuccess'
def RemoveShareData(key):
	'''移除共享数据'''
	return 'ifsuccess'
def ToMD5(text):
	'''返回test对应的md5值'''
	return 'MD5'
def WorkingPath():
	'''返回bds的完整工作路径'''
	return 'WorkingPath'
def HttpPost(url,data):
	'''发起一个httpPost请求'''
	return 'PostData'
def HttpGet(url,data):
	'''发起一个httpGet请求'''
	return 'GetData'
def CreateDir(path):
	'''创建文件夹'''
	pass
def IfFile(path):
	'''判断文件是否存在'''
	return 'bool'
def IfDir(path):
	'''判断文件夹是否存在'''
	return 'bool'
def ShareFunc(key,func):
    '''共享一个函数'''
    pass
def GetShareFunc(key):
    '''获得一个共享函数'''
    return 'ShareFunc'
def ThrowException(msg):
    '''抛出一个可以被捕获的异常'''
    pass