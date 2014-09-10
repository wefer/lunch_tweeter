#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib2
import re
import datetime

def get_content(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	page_content = response.read()
	return page_content



def get_nanna_menu(day):
	page_content = get_content('http://restaurang-ns.com/restaurang-nanna-svartz/')

	weekdays = ['Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag']

	menu = '\n'.join([x.split('<')[0] for x in re.findall(weekdays[day]+'(.*?)<strong>', page_content, re.DOTALL|re.M)[0].split('<p>')[1:-2]])

	return menu

def get_konigs_menu(day):
	page_content = get_content('http://restaurangkonigs.se')

	weekdays = ['Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag']

	menu = '\n'.join([x.split('>')[-1] for x in re.findall(weekdays[day]+'(.*?)</p>', page_content, re.DOTALL|re.M)[0].split('<br />')])

	return menu


def main():

	current_day = datetime.datetime.today().weekday()
	print "\nDagens lunch Nanna Svartz:\n--------------------------\n", get_nanna_menu(current_day), "\n\nDagens lunch SMI:\n--------------------------\n", get_konigs_menu(current_day), '\n'


if __name__ == "__main__":
	main()

