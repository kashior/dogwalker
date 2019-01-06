# -------------------------------------------------------------------------------
# Web Users
# -------------------------------------------------------------------------------
# A class to manage the Users registertion - create and save in the DB
#-------------------------------------------------------------------------
# Author:       Nurit Agami ,Shalev Levy ,Oriana Messika
# Last updated: 26.12.2018
#-------------------------------------------------------------------------

# import logging so we can write messages to the log
import datetime
import logging
import db_handler # import the class DbHandler to interact with the database
from google.appengine.api import users





class RegisterUser():
	def __init__(self,name,mail_address,phone_no1,phone_no2,city):
		self.name=name
		self.mail_address=mail_address
		self.Phone_number=[phone_no1,phone_no2]
		self.city=city
		self.m_DbHandler=db_handler.DbHandler()
		self.db_id=''
		
		

class DogWalker(RegisterUser):
	def __init__(self,name,mail_address,phone_no1,phone_no2,city,work_days,payment_per_walk,breeds_handle,max_no_of_dogs_per_day):
		RegisterUser.__init__(self,name,mail_address,phone_no1,phone_no2,city)
		self.works_days=work_days
		self.payment_per_walk=int(payment_per_walk)
		self.breeds_handle=breeds_handle
		self.max_no_of_dogs_per_day=int(max_no_of_dogs_per_day)
	
	
	def insertToDb(self):
		logging.info('In DogWalker.insertToDb')
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		sql = 	"""
				INSERT INTO Dogwalker(Users_name,Mail_address,City,payment_per_walk,max_no_of_dogs_per_date) 
				VALUES(%s,%s,%s,%s,%s)
				"""
		logging.info('executing sql')
		cursor.execute( sql, 
						(self.name,self.mail_address,self.city,self.payment_per_walk,self.max_no_of_dogs_per_day ))
		self.db_Id = cursor.lastrowid
		self.m_DbHandler.commit()
		logging.info("finished dogwalker insert")
		tables={'Dogwalker_Phone_numbers':[self.Phone_number,'Phone_number'],'Dogwalkers_works_days':[self.works_days,'works_days'],'Dogwalkers_breeds_handle':[self.breeds_handle,'breeds_handle']}
		for key in tables.keys():
			command='INSERT INTO '+key+ '('+tables[key][1]+',Mail_address) VALUES (%s, %s)'
			data=self.prepare_data(tables[key][0])
			cursor.executemany(command, data)
			self.m_DbHandler.commit()
		
		self.m_DbHandler.disconnectFromDb()
		logging.info('user created id is  '+ str(self.db_Id))
		return
		
		
		
		
	def prepare_data(self,lst):
		data=[]
		for i in range(len(lst)):
			if lst[i]:
				temp=(lst[i],self.mail_address)
				data.append(temp)
			else:
				continue
		return data
			
			
			
			
class DogOwner(RegisterUser):
	def __init__(self,name,mail_address,phone_no1,phone_no2,city):
		RegisterUser.__init__(self,name,mail_address,phone_no1,phone_no2,city)		
		self.register_date=''
		


class DogOwnerRegular(DogOwner):
	def __init__(self,name,mail_address,phone_no1,phone_no2,city):
		DogOwner.__init__(self,name,mail_address,phone_no1,phone_no2,city)
		self.fee_per_month=20
	
	def insertToDb(self):
		logging.info('In DogOwnerRegular.insertToDb')
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		self.register_date=datetime.datetime.now()
		logging.info(self.register_date)
		sql = 	"""
				INSERT INTO Regular(Users_name,Mail_address,city,fee_per_month,register_date) 
				VALUES(%s,%s,%s,%s,%s)
				"""
		cursor.execute( sql, 
						(self.name,self.mail_address,self.city,self.fee_per_month,self.register_date))
		self.db_Id = cursor.lastrowid
		self.m_DbHandler.commit()
		command='''INSERT INTO Regular_Phone_numbers(Mail_address,Phone_numbers) 
				VALUES(%s,%s)'''
		data=[(self.mail_address,self.Phone_number[0]),(self.mail_address,self.Phone_number[1])]
		if not data[1][1]:
			cursor.execute(command, data[0])
		else:
			cursor.executemany(command, data)
		self.m_DbHandler.commit()
		self.m_DbHandler.disconnectFromDb()
		logging.info('user created id is  '+ str(self.db_Id))
		return
	
	
"""class DogOwnerPremuim(DogOwner):
	def __init__(self):
		DogOwner.__init__(self)
		self.fee_per_year=300
	
	def insertToDb(self):
		logging.info('In DogOwnerPremuim.insertToDb')
		self._DbHandler.connectToDb()
		cursor=self._DbHandler.getCursor()
		self.register_date=sysdate()
		sql ='INSERT INTO DogOwnerPremuim(name,mail_address,city,fee_per_year) VALUES(%s,%s,%s,sysdate())'
				  
		cursor.execute( sql, 
						(self.name,self.mail_address,self.city,self.fee_per_year,register_date))
		self.db_Id = cursor.lastrowid
		self._DbHandler.commit()
		command='''INSERT INTO phone_no(mail_address,phone_no) 
				VALUES(%s,%s)'''
		data=[(self.mail_address,self.phone_no[0]),(self.mail_address,self.phone_no[1])]
		if not data[1][1]:
			cursor.execute(command, data[0])
		else:
			cursor.executemany(command, data)
		cursor.executemany(command, data)
		self._DbHandler.commit()
		self._DbHandler.disconnectFromDb()
		logging.info('user created id is  '+ str(self.db_Id))
		return"""
		
def get_dogs_from_user():
	logging.info('get_dogs_from_user')
	user=users.get_current_user()
	if not user:
		return []
	mail=user.email()
	#creating a new DbHandler object for connecting to the DB
	db=db_handler.DbHandler()
	db.connectToDb()
	cursor=db.getCursor()
	sql =   """select Dogs_name from Dog where R_Mail_address=%s"""
	
	cursor.execute(sql,(mail,))
	return cursor.fetchall()
	
def Is_already_registered():
	logging.info('Is_already_registered')
	user=users.get_current_user()
	if not user:
		return 3
	mail=user.email()
	#creating a new DbHandler object for connecting to the DB
	db=db_handler.DbHandler()
	db.connectToDb()
	cursor=db.getCursor()
	
	
	sql_dogowner =   """select count(*)from Regular where Mail_address=%s"""
	
	cursor.execute(sql_dogowner,(mail,))
	in_db=cursor.fetchone()
	if in_db[0]>0: #the user is already registered as a dog owner
		db.disconnectFromDb()
		return 1 # 1 means dog owner
	else:
		sql_dogwalker =   """select count(*)from Dogwalker where Mail_address=%s"""
		cursor.execute(sql_dogwalker,(mail,))
		in_db_dw=cursor.fetchone()
		if in_db_dw[0]>0:#the user is already registered as a dog walker
			db.disconnectFromDb()
			return 2 # 2 means dog walker
		else:
			return 0 # user is not registered
def get_dog_walkers(city=None,days=None):
	logging.info('get_dog_walkers')
	user=users.get_current_user()
	if not user:
		return []
	mail=user.email()
	#creating a new DbHandler object for connecting to the DB
	db=db_handler.DbHandler()
	db.connectToDb()
	cursor=db.getCursor()
	dogwalkers=[]
	if not city and not days:
		sql = """select Users_name,Mail_address,City from Dogwalker"""
		cursor.execute(sql)
		return cursor.fetchall()
	elif not days:
		sql= """select Users_name,Mail_address,City from Dogwalker where Dogwalker.city=%s"""
		cursor.execute(sql,(city,))
		return cursor.fetchall()
	elif not city:
		for day in days:
			sql= """select Dogwalker.Users_name,Dogwalker.Mail_address,Dogwalker.City from Dogwalker,Dogwalkers_works_days
			where Dogwalkers_works_days.works_days=%s and Dogwalker.Mail_address=Dogwalkers_works_days.Mail_address"""
			cursor.execute(sql,(day,))
			current_dogwalkers=cursor.fetchall()
			for dw in current_dogwalkers:
				if dw not in dogwalkers:
					dogwalkers.append(dw)
	else:
		for day in days:
			logging.info('day is {}'.format(day))
			sql= """select Dogwalker.Users_name,Dogwalker.Mail_address,Dogwalker.City from Dogwalker,Dogwalkers_works_days
			where Dogwalkers_works_days.works_days=%s and Dogwalker.Mail_address=Dogwalkers_works_days.Mail_address and Dogwalker.city=%s"""
			cursor.execute(sql,(day,city,))
			current_dogwalkers=cursor.fetchall()
			for dw in current_dogwalkers:
				if dw not in dogwalkers:
					dogwalkers.append(dw)
	return dogwalkers
	
def is_register_valid(day,dogwalker):
	logging.info('is_register_valid')
	user=users.get_current_user()
	if not user:
		return False
	mail=user.email()
	#creating a new DbHandler object for connecting to the DB
	db=db_handler.DbHandler()
	db.connectToDb()
	cursor=db.getCursor()
	logging.info(dogwalker[1])
	sql_day="""select count(*) from Dogwalkers_works_days where Dogwalkers_works_days.works_days=%s and Dogwalkers_works_days.Mail_address=%s"""
	cursor.execute(sql_day,(day,dogwalker[1],))
	if int(cursor.fetchone()[0]) == 0:
		logging.info("NO DOG WALKERS SUITABLE1")
		return False
	sql= """select count(*) from dogs_registered_for_walk where dogs_registered_for_walk.day_in_week=%s and dogs_registered_for_walk.dog_walker_mail=%s"""
	cursor.execute(sql,(day,dogwalker[1],))
	num_of_dogs_in_day=cursor.fetchone()[0]
	sql_max="""select max_no_of_dogs_per_date from Dogwalker where Dogwalker.Mail_address=%s"""
	cursor.execute(sql_max,(dogwalker[1],))
	if num_of_dogs_in_day<int(cursor.fetchone()[0]):
		return True
	logging.info("NO DOG WALKERS SUITABLE2")
	return False

	
