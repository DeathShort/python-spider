# -*- coding: utf-8 -*-
import urllib2
import json
import datetime
import chardet
from pandas.io.json import json_normalize
import pandas as pd

# print jsonstr
def pages_num():
	url = "http://data.eastmoney.com/DataCenter_V3/yjfp/getlist.ashx?js=var%20gFOPZimo&pagesize=50" \
		  "&page=1&sr=-1&sortType=SZZBL&mtk=%C8%AB%B2%BF%B9%C9%C6%B1&filter=(ReportingPeriod=^2016-12-31^)&rt=49634723"
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	data = response.read().decode('gbk')
	start_pos = data.index('=')
	json_data = data[start_pos+1:]
	dict = json.loads(json_data)
	pages = dict['pages']
	return pages
#get the url_list
def get_urls():
	url_list=[]
	start = 1
	while(start<=pages_num()):
		url = "http://data.eastmoney.com/DataCenter_V3/yjfp/getlist.ashx?js=var%20gFOPZimo&pagesize=50"
		url+="&page=%d"%start
		url+="&sr=-1&sortType=SZZBL&mtk=%C8%AB%B2%BF%B9%C9%C6%B1&filter=(ReportingPeriod=^2016-12-31^)&rt=49634723"
		url_list.append(url)
		start += 1
	return url_list
#create target file
today =datetime.date.today()
str_date = '%Y%m%d'
str_today = today.strftime(str_date)
headers = ['代码','名称','送转总比例','送股比例','转股比例','现金分红比例','股息率','预案公告日','总股本','每股收益','每股净资产',
		   '每股公积金','每股未分配利润','净利润同比增长','方案进度','分红配股方案']
columns = ['Code','Name','SZZBL','SGBL','ZGBL','XJFH','GXL','YAGGR','TotalEquity','EarningsPerShare',
		   'NetAssetsPerShare','MGGJJ','MGWFPLY','JLYTBZZ','ProjectProgress','AllocationPlan']
f = open('D:/stock_profit/stock_profit_%s.xlsx' % str_today,'a+')
f.close()
#main
url_list = get_urls()
bd = pd.DataFrame()
for url in url_list:
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	data = response.readline()
	encoding = chardet.detect(data)['encoding']
	data = data.decode(encoding,'ignore')
	start_pos = data.index('=')
	json_data = data[start_pos+1:]
	print json_data
	dict = json.loads(json_data)
	ad = json_normalize(dict['data'])
	bd = bd.append(ad,ignore_index=True)
print bd
#write data to excel
# pd.DataFrame.to_excel(bd,excel_writer='D:/stock_profit/stock_profit_%s.xlsx' % str_today,index=None,
# 					  columns=[1,2,3,4,5,6,7,8,15,16,17,18,19,20,23,24],header=headers)
# pd.DataFrame.to_excel(bd,excel_writer='D:/stock_profit/stock_profit_%s.xlsx' % str_today,index=None)
pd.DataFrame.to_excel(bd,excel_writer='D:/stock_profit/stock_profit_%s.xlsx' % str_today,index=None,columns=columns,
					  header=headers)