# -*- coding:utf-8 -*-
import requests
import sys
import io
from bs4 import BeautifulSoup
import pymysql as p
import re
import json


reload(sys)
sys.setdefaultencoding('utf-8')


'''
url1 = "http://www.51job.com" #success

headers={
'Host':'www.51job.com',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive',
'Accept-Language':'en-us',
'Accept-Encoding':'gzip, deflate',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
'Cookie':'',
'Upgrade-Insecure-Requests':'1'
}



r = requests.get(url2,headers=headers)
r.encoding='gbk'
f = io.open('myScrapy3.html','w')
f.write(r.text)
f.close()
'''


'''
url2 = "https://ehire.51job.com"
headers={
'Referer':'http://www.51job.com/',
'Host':'ehire.51job.com',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive',
'Accept-Language':'en-us',
'Accept-Encoding':'br, gzip, deflate',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
'Cookie':''
}
r = requests.get(url2, headers=headers)
r.encoding='utf-8'
f = io.open('myScrapy3_2.html','w',encoding='utf-8')
f.write(r.text)
f.close()
'''



headers={
'Referer':'https://ehire.51job.com/',
'Host':'ehire.51job.com',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive',
'Accept-Language':'en-us',
'Accept-Encoding':'br, gzip, deflate',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
'Cookie':''
}





#utils
def saveHtml(filename, content):
	f = io.open(filename,'w',encoding='utf-8')
	f.write(content)
	f.close()
	
	
#success
url3 = "https://ehire.51job.com/Navigate.aspx?ShowTips=11&PwdComplexity=N"

headers={
'Referer':'https://ehire.51job.com/',
'Host':'ehire.51job.com',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive',
'Accept-Language':'en-us',
'Accept-Encoding':'br, gzip, deflate',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
'Cookie':''
}

html = requests.get(url3, headers=headers)
html.encoding = "utf-8"
#f = io.open("myScrapy3_4.html" , "w", encoding="utf-8")
#f.write(html.text)
#f.close()
#main = f.readlines()

#InboxResume/InboxNavigator.aspx

prefix = 'https://ehire.51job.com'
soup = BeautifulSoup(open('myScrapy3_4.html'))
''' 
# 2 - enter all resume

for link in soup.find_all('a'):
	if (link.string == '查看简历'):
		resume = prefix+link.get('href')
		r = requests.get(resume,headers=headers)
		r.encoding='utf-8'
		f = io.open('myScrapy3_5.html','w',encoding='utf-8')
		f.write(r.text)
		f.close()
'''	

# 3- enter resume list
soup2 = BeautifulSoup(open('myScrapy3_5.html'))
for li in soup2.find_all('li',class_="tb-name-c ev-tb-name-c ev-li"):
	#获得名字
	name = li.string
	#获得简历链接
	href = li.find('a').get('href')

	#名字插入数据库
	db = p.connect('localhost','root','dragon','hr',charset='utf8')
	cur = db.cursor()
	sql = """insert into applicants(name) values('%s');"""
	effect_row = cur.execute(sql % (name))
	db.commit()
	
	#保存简历
	single = requests.get(prefix+href,headers=headers)
	single.encoding='utf-8'
	'''
	saveHtml('mySrapy3_single_' + name +'.html',single.text)
	'''
	
	#爬虫简历
	soup3 = BeautifulSoup(single.text)
	man = {}
	#邮箱
	infos = soup3.find_all('a')
	for info in infos:
		if re.search('mailto:',str(info.get('href'))):
			man['email'] = str(info.get('href'))[7:]
	
	
	infos = soup3.find_all('img')
	for info in infos:
		src = info.get('src')
		#电话
		if re.search('y2.png', str(src)):
			
			man['phone'] = info.parent.get_text()

		
		if re.search('y4.png', str(src)):
			all = info.parent.get_text().strip()
			#性别
			man['sex'] = all[0:1]
			#出生日期			
			r = re.findall('.*\((.*)\s.*',all)
			string = "xxxxxxxxxxxxxxxxxxxxxxxx entry '某某内容' for aaaaaaaaaaaaaaaaaa"
			r= re.findall(".*entry(.*)for.*",string)
			r.encode('utf-8')
		
			print(r)
			
			#查看结果
			print(json.dumps(man, encoding='utf-8', ensure_ascii=False))

			
		
			
	

	

			
			
			


	
	


	
	
	



'''
r = requests.get('https://github.com/timeline.json')
requests.post('https://github.com/timeline.json')
requests.put('https://github.com/timeline.json')
requests.delete('https://github.com/timeline.json')
requests.head('https://github.com/timeline.json')
requests.options('https://github.com/timeline.json')

payload = {'key1':'value1','key2':'value2'}
r = requests.get('https://github.com/timeline.json',params=payload)
#print(r.url)
r = requests.get('https://github.com/timeline.json')
#print(r.text)
print(r.content)
'''


'''
import sys, urllib2  
  
req = urllib2.Request(sys.argv[1])  
fd = urllib2.urlopen(req)  
print "Retrieved", fd.geturl()  
info = fd.info()  
for key, value in info.items():  
    print "%s = %s" % (key, value)
'''



