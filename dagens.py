#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib2
import re
import datetime
import tweet

def get_content(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	page_content = response.read()
	return page_content



def get_nanna_menu(day):
	page_content = get_content('http://restaurang-ns.com/restaurang-nanna-svartz/')

	rest_name = "NANNA SVARTZ"

	weekdays = ['Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag']
	weekday = weekdays[day]

	menu = '\n'.join([x.split('<')[0] for x in re.findall(weekdays[day]+'(.*?)<strong>', page_content, re.DOTALL|re.M)[0].split('<p>')[1:-2]])

	return [rest_name, weekday, menu]

def get_konigs_menu(day):
	page_content = get_content('http://restaurangkonigs.se')

	rest_name = "SMI"

	weekdays = ['Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag']
	weekday = weekdays[day]

	menu = '\n'.join([x.split('>')[-1] for x in re.findall(weekdays[day]+'(.*?)</p>', page_content, re.DOTALL|re.M)[0].split('<br />')])

	return [rest_name, weekday, menu]


def main():

	current_day = datetime.datetime.today().weekday()
	tweet.tweet("/home/hw/work/lunch_tweeter/tw.yaml",  get_konigs_menu(current_day))
	tweet.tweet("/home/hw/work/lunch_tweeter/tw.yaml", get_nanna_menu(current_day))
if __name__ == "__main__":
	main()

