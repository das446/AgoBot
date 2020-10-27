import discord
import time
import asyncio
import csv
import sys
from discord.ext import commands, tasks
import configparser
from datetime import datetime
from security import is_admin_channel, is_in_channel, Error
import os
import random
import typing
import qrcode
import io
import socket

from selenium import webdriver 
from time import sleep 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options  
from html.parser import HTMLParser

class Event:
	def __init__(self, name, time, imgurl, url):
		self.name = name
		self.time = time
		self.imgurl = imgurl
		self.url = url
		
	def ToEmbed(self):
		embed = discord.Embed(title=self.name, colour=discord.Colour(0xc663a9), url=self.url)
		embed.set_image(url=self.imgurl)
		embed.set_footer(text=self.time)
		return embed

def GetFbLogin(settings):
	if settings.environment == "prod":
		aws = settings.config.read('config')
		user = os.environ['FB_USER']
		pw = os.environ["FB_PW"]
		return user, pw
	
	else:
		return input("Enter Email "), input("Enter Password ")


def GetEvents(settings):
	usr, pwd = GetFbLogin(settings)
	
	
	driver = ""
	if settings.environment=="prod":
		CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
		GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
		
		
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')
		chrome_options.binary_location = GOOGLE_CHROME_BIN
		
		driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
	
	else:
		driver = webdriver.Chrome(ChromeDriverManager().install())
		
	tag = ''
	try:
		
		driver.get('https://www.facebook.com/groups/DrexelAGO/events')
		print ("Opened facebook")
		sleep(1)
		
		username_box = driver.find_element_by_id('email')
		username_box.send_keys(usr)
		print ("Email Id entered")
		sleep(1)
		
		password_box = driver.find_element_by_id('pass')
		password_box.send_keys(pwd)
		print ("Password entered")
		
		login_box = driver.find_element_by_id('loginbutton')
		login_box.click()
		sleep(10)

		#new events only
		
		tag = "fbCalendarList"
		
		dates = driver.find_elements_by_class_name(tag)
		
		tag = "fbCalendarItemContent"
		
		events = driver.find_elements_by_class_name(tag)
		
		eventObjects = []
		


		for event, date in zip(events, dates):
		
			e = event.find_element_by_xpath("//div")
			
			a = e.find_element_by_xpath("//a")
			
			url = "https://www.facebook.com" + str(a.get_attribute('href'))
			
			bg = a.find_element_by_xpath("//img").get_attribute("src")
			
			tag = "uiHeaderTitle"

			d = str(date.find_element_by_class_name(tag).get_attribute('innerHTML'))

			title = a.find_element_by_xpath("//img").get_attribute('aria-label')
			
			eventObject = Event(name = str(title), time = str(d), imgurl = str(bg), url = str(url))
			eventObjects.append(eventObject)
			
	except:
		f = open("error.html", "w+")
		f.write(driver.find_element_by_xpath("//body").get_attribute('innerHTML'))
		f.close()
		
		file = discord.File("error.html", filename="error.html")
		raise Error("Couldn't find element " + tag + " on page", file=file)
	
	driver.quit()
	return eventObjects




class FaceBook(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		#self.Loop.start()
	
	"""
	@tasks.loop(seconds=300)
	async def Loop(self):
		await OnLoop(self.bot)
		
	@Loop.before_loop
	async def pre_loop(self):
		await self.bot.wait_until_ready()
	"""

	@commands.command(name='events', help='Show upcoming events.', pass_context=True)
	async def ShowEvents(self, ctx):
		async with ctx.typing():
			events = GetEvents(self.bot.settings)
			
			for event in events:
				embed = event.ToEmbed()
				await ctx.send(embed=embed)
		