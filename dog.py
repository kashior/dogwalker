

import logging
# import the class DbHandler to interact with the database
import db_handler
from google.appengine.api import users


class Dog():
	def __init__(self,Dogs_name,Gender,Age,breed_name,R_Mail_address):
		logging.info('Initializing dog')
		self.Dogs_no=''
		self.R_Mail_address=R_Mail_address
		self.breed_name=breed_name
		self.Age=Age
		self.Gender=Gender
		self.Dogs_name=Dogs_name
		self.m_DbHandler=db_handler.DbHandler()
		
		
	def insertToDb(self):
		logging.info('In Dog.insertToDb')
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		sql = 	"""
				INSERT INTO Dog(Dogs_name,Gender,Age,breed_name,R_Mail_address) 
				VALUES(%s,%s,%s,%s,%s)
				"""
		cursor.execute( sql, 
						(self.Dogs_name,self.Gender, self.Age,self.breed_name,self.R_Mail_address))
		self.Dogs_no = cursor.lastrowid
		self.m_DbHandler.commit()
		self.m_DbHandler.disconnectFromDb()
		logging.info('Dog created id is  '+ str(self.Dogs_no))
		return




	
	def SignDogToDogwalker():
		logging.info('in SignDogToDogwalker')
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		sql ="""
				INSERT INTO schedualing_list_of_day_per_day(Day_in_week,Mail_address,Dogs_no) 
				VALUES(%s,%s,%s)
				"""
		cursor.execute( sql, 
						(Day_in_week,Mail_address, self.Dogs_no)) #the mail_address is the dogwalker's
		self.m_DbHandler.commit()
		self.m_DbHandler.disconnectFromDb()
	
	
	
	
	
	
	
	
	
		
		
		
	