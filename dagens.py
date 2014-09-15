#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
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

        soup = BeautifulSoup(page_content)

        weekdays = [ "Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag" ]

        d = { "Måndag" : [], "Tisdag" : [], "Onsdag" : [], "Torsdag" : [], "Fredag" : [] }

        curr_key = None

        for line in soup.findAll("div", {"class" : "span6"})[0].text.split('\n'):
                d_flag = 0 
                for key in d.keys():
                        if key.decode('utf-8') in line:
                                curr_key = key 
                                d_flag = 1 
                if not curr_key:
                        continue
                else:
                        if d_flag != 1:
                                d[curr_key].append(line)

        weekday = weekdays[day]
        menu = '\n'. join(d[weekday]).rstrip()
    
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
	tweet.tweet("/home/hugo/lunch_tweeter/tw.yaml",  get_konigs_menu(current_day))
	tweet.tweet("/home/hugo/lunch_tweeter/tw.yaml", get_nanna_menu(current_day))
if __name__ == "__main__":
	main()

