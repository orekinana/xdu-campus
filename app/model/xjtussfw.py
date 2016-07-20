# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re
from HTMLParser import HTMLParser
from xjtu_grade_parser import *

class XJTU:

	def __init__(self):
		# URL for login
		self.loginUrl = 'https://cas.xjtu.edu.cn/login?service=http%3A%2F%2Fssfw.xjtu.edu.cn%2Findex.portal'
		# URL of grades
		self.gradeUrl = 'http://ssfw.xjtu.edu.cn/index.portal?.pn=p1142_p1144_p1156'
		# Simulating Browser
		self.headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'
		}
		self.cookies = cookielib.CookieJar()
		self.postdata = urllib.urlencode({})
		
		# Generate opener
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))

	# Get grades page
	def get_page(self, lt, exe):

		# Generate POST data
		self.postdata = urllib.urlencode({
			'username':'zdzhu',
			'password':'zdzhu123456',
			'lt':lt,
			'execution':exe,
			'_eventId':'submit',
		})

		# POST data
		request  = urllib2.Request(
			url = self.loginUrl,
			data = self.postdata,
			headers = self.headers)
		result = self.opener.open(request)
		# Get direct URL
		html = result.read().decode('utf-8')
		pattern = re.compile(r"ct\('(.+?)'")
		url = re.findall(pattern, html)

		# Direct URL
		result = self.opener.open(url[0])

		# Get grades page
		result = self.opener.open(self.gradeUrl)
		return result.read()

	# get the keys for login
	def get_keys(self):
		result = self.opener.open(self.loginUrl)
		html = result.read().decode('utf-8')
		pattern = re.compile(r'type="hidden".+value="(.+?)"')
		values = re.findall(pattern, html)
		return values[0], values[1]

if __name__ == '__main__':
	xjtu = XJTU()
	lt, exe = xjtu.get_keys()
	html = xjtu.get_page(lt, exe)
	xjtuGradeParser = XjtuGradeParser()
	grades = xjtuGradeParser.html_parser(html)
	for grade in grades:
		print grade.name, grade.grades['main']