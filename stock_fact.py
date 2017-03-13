# -*- coding: utf-8 -*-
import urllib2
import json
import datetime
import pandas as pd

'''
根据url的response可以看出，这是一个js文件，可以将其转变为json格式后再进行处理。
'''
def pages_num():
	url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=C" \
		  "&sortRule=-1&page=1&pageSize=20&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}" \
		  "&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.5072298033821419"
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	data = response.read()
	start_pos = data.index('=')
	js_object = data[start_pos + 1:]
	# print js_object[0] + '"' +js_object[1:5] + '"' + js_object[5:-10] + '"' +js_object[-10:-5] +'"' +js_object[-5:]
	json_data = js_object[0] + '"' + js_object[1:5] + '"' + js_object[5:-10] + '"' + js_object[ -10:-5] + '"' \
				+ js_object[-5:]
	dict = json.loads(json_data)
	pages = dict['pages']
	return pages

#获取url池
def get_urls():
	url_list = []
	start = 1
	while (start <= pages_num()):
		url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA"
		url += "&sortType=C&sortRule=-1&page=%d&pageSize=20" % start
		url += "&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c"
		url += "&jsName=quote_123&_g=0.5072298033821419"
		url_list.append(url)
		start += 1
	return url_list

#创建文件，文件名根据当前系统日期生成。文件目录可以自己更改，应该可以自动生成，但是这里没有去实现
today =datetime.date.today()
str_date = '%Y%m%d'
str_today = today.strftime(str_date)
headers = ['代码','名称','最新价','涨跌额','涨跌幅','振幅（%）','成交量（手）','成交额','昨收','今开','最高','最低',
		   '量比','换手（%）','市盈']
f = open('D:/stock_profit/stock_pool_%s.xlsx' % str_today,'a+')
f.close()

'''
主程序，因为获取的数据是list里的string，没有key，pandas生成dataframe的时候是没有列头的，
可以使用列的index选择要储存的列，并用header重命名
'''
url_list = get_urls()
print url_list
bd = pd.DataFrame()
for url in url_list:
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	data = response.read()
	start_pos = data.index('=')
	js_object = data[start_pos + 1:]
	json_data = js_object[0]+'"'+js_object[1:5]+'"'+js_object[5:-10] + '"' + js_object[-10:-5] + '"' + js_object[-5:]
	dict = json.loads(json_data)
	list = dict['rank']
	pd_data = []
	for x in list:
		stock_meg = x.split(',')
		stock_pool = []
		for y in stock_meg:
			stock_pool.append(y)
		pd_data.append(stock_pool)
	df = pd.DataFrame(pd_data)
	bd = bd.append(df,ignore_index=True)
print bd
#write data to excel
pd.DataFrame.to_excel(bd,excel_writer='D:/stock_profit/stock_pool_%s.xlsx' % str_today,index=None,
					  columns=[1,2,3,4,5,6,7,8,9,10,11,12,22,23,24],header=headers)