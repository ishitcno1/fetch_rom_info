"""Script for fetching rom info from freeroms.com

Functions:
	parse_rom_page(rom_page_url) -> list
	parse_rom_list(rom_list_url) -> [(str, str), (str, str)]

Arguments:
	init -- if give argument init will init database

"""

import urllib2
import re
import sqlite3
import sys
from bs4 import BeautifulSoup


def parse_rom_page(rom_page_url):
	"""Parse rom page.

	Arguments:

	rom_page_url -- rom page url

	Return values:

	Rom list urls from A to Z
	"""
	rom_page = urllib2.urlopen(rom_page_url).read()
	soup = BeautifulSoup(rom_page)
	all_a = soup.findAll('a', href=re.compile("_A.htm$"))
	target_a = all_a[0].parent.findAll('a')[1:27]
	rom_list_urls = []
	for a in target_a:
		rom_list_urls.append(a['href'])
	return rom_list_urls

def parse_rom_list(rom_list_url):
	"""Parse rom list.

	Arguments:

	rom_list_url -- rom list url

	Return values:

	A list contains (rom_name, rom_download_page) tuples.
	"""
	print "Parsing rom list %s." % rom_list_url[-5]
	rom_list = urllib2.urlopen(rom_list_url).read()
	soup = BeautifulSoup(rom_list)
	target_a = soup.findAll('a', href=re.compile("^http://www.freeroms.com/roms/"))
	rom_name_and_download_page = []
	for a in target_a:
		rom_name = str(a.string)
		rom_download_page = a['href']
		rom_name_and_download_page.append((rom_name, rom_download_page))
	return rom_name_and_download_page

def fetch_rom_info(rom_type):
	"""Fetch rom info and store in database rom_info.db.

	Arguments:

	rom_type -- rom type

	"""
	rom_page_urls = {"gbc": "http://www.freeroms.com/gameboy_color.htm", 
		"gba" :"http://www.freeroms.com/gameboy_advance.htm",
		"nes" :"http://www.freeroms.com/nes.htm",
		"snes" :"http://www.freeroms.com/snes.htm"}
	rom_page_url = rom_page_urls[rom_type]
	rom_list_urls = parse_rom_page(rom_page_url)

	db = sqlite3.connect("rom_info.db")
	cur = db.cursor()
	for rom_list_url in rom_list_urls:
		rom_name_and_download_page = parse_rom_list(rom_list_url)
		for rom_name, rom_download_page in rom_name_and_download_page:
			sql_statement = """INSERT INTO rom_info(name, download_page, rom_type) \
				VALUES("%s", "%s", "%s")""" % (rom_name, rom_download_page, rom_type)
			cur.execute(sql_statement)
	db.commit()
	cur.close()
	db.close()

def init_database():
	"""Init database rom_info.db.

	"""
	db = sqlite3.connect("rom_info.db")
	cur = db.cursor()
	cur.execute("CREATE TABLE rom_info(id integer PRIMARY KEY, name TEXT, \
		download_page TEXT, download_url TEXT, rom_type TEXT, description TEXT)")
	db.commit()
	cur.close()
	db.close()

if __name__ == '__main__':
	rom_types = ['gbc', 'gba', 'nes', 'snes']
	if len(sys.argv) > 1 and sys.argv[1] == 'init':
		init_database()
	elif len(sys.argv) == 1:
		for rom_type in rom_types:
			print 'Fetching %s info.' % rom_type
			fetch_rom_info(rom_type)
	else:
		print "Invalid argument."

