# -------------------------------------------------------------------------------
# Hello user - Using HTML with Jinja
# -------------------------------------------------------------------------------
# The application demonstrates how to use HTML inside the Python code 
# using jinja2
# This allows us to separate the formatting (HTML) from the code (Python)
# If we call the application http://localhost:16080/ - the main page will show
# 3 links
# /show_status - A message with the login status will be shown
# /login       - The user will be prompted to perform login to google
# /logout      - The user will be logged out from the google account
#-------------------------------------------------------------------------
# Author:       Nurit Agami , Shalev Levy ,Oriana Messika
# Last updated: 13.01.2019
#-------------------------------------------------------------------------


# import webapp2  - Python web framework compatible with Google App Engine
import webapp2
# import the users library from google
from google.appengine.api import users
# import logging so we can write messages to the log
import logging
import web_users
import dog
#import Jinja and os libraries
import jinja2
import os
import db_handler

#Load Jinja
jinja_environment =jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
type_user=''
# ---------------------------------------------------------
# Main page - show links to - Show status, login and logout 
# Handles /
# --------------------------------------------------------
class MainPage(webapp2.RequestHandler):
    def get(self):   
		user = users.get_current_user()
		x = web_users.Is_already_registered()
		parameters_for_template = {'user': user,'type_user': x}
		main_page_template = jinja_environment.get_template('main_page.html')
		self.response.write(main_page_template.render(parameters_for_template))


# -----------------------------------------
# class to show the status - logged in or logged out
# if logged in
# 	We will use HTML file to display the values from the user object
# if logged out
#   You are logged out
# Handles /show_status 
# -----------------------------------------

class Login(webapp2.RequestHandler):
    def get(self):
        # Checks if the user is logged in
		user = users.get_current_user()
        # if logged in
		if user:
			is_registerd=web_users.Is_already_registered()
			if is_registerd==1:  #dog owner
				self.redirect('/')
			elif is_registerd==2 :#dog walker
				self.redirect('/')
			else:
				define_user_template = jinja_environment.get_template('define_user.html')
				self.response.write(define_user_template.render())
				
		else:
			self.redirect(users.create_login_url('/register'))
            
      

# ------------------------------------------------------
# class to handle /login requests
# will force the user to perform login and will show the status
# ------------------------------------------------------

		
class SentDogInfo(webapp2.RequestHandler):
	def post(self):
		global type_user
		user = users.get_current_user()
		R_Mail_address=user.email()
		breed_name=self.request.get('breed')
		logging.info("breed name is {}".format(breed_name))
		Age=self.request.get('age')
		Gender=self.request.get('gender')
		Dogs_name=self.request.get('name')
		users_dog=dog.Dog(Dogs_name,Gender,Age,breed_name,R_Mail_address)
		users_dog.insertToDb()
		parameters_for_template={'type_user':type_user}
		congrats = jinja_environment.get_template('congrats.html')
		self.response.write(congrats.render(parameters_for_template))
		

class Register(webapp2.RequestHandler):
	def get(self):
		is_registerd=web_users.Is_already_registered()
		if is_registerd==1:  #dog owner
			self.redirect('/')
		elif is_registerd==2 :#dog walker
			self.redirect('/')
		else:
			define_user_template = jinja_environment.get_template('define_user.html')
			self.response.write(define_user_template.render())

class RegisterDog(webapp2.RequestHandler):
	def get(self):
		list_of_breeds=['Beagle','Bulldog','Chihuahua','German_Shepherd','Labrador_Retriever','Poodle','Siberian_Husky']
		parameters_for_template={'list_of_breeds':list_of_breeds}
		reg_dog_template=jinja_environment.get_template('register_your_dog.html')
		self.response.write(reg_dog_template.render(parameters_for_template))
		
		
class SentType(webapp2.RequestHandler):
	def post(self):
		global type_user
		user = users.get_current_user()
		list_of_breeds=['Beagle','Bulldog','Chihuahua','German Shepherd','Labrador Retriever','Poodle','Siberian Husky']
		list_of_days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
		list_of_cities=['Tel-Aviv','Jerusalem','Haifa','Eilat','Bat-Yam','Netanya','Ramat-Hasharon','Zichron-Yaakov','Holon','Hadera','Afula','Netivot']
		type_user=self.request.get('type_user')
		parameters_for_template = {'type_user': type_user,'user': user,'list_of_days' :list_of_days,'list_of_cities':list_of_cities,'list_of_breeds' :list_of_breeds}
		register_template = jinja_environment.get_template('register.html')
		self.response.write(register_template.render(parameters_for_template))


class SentRegistration(webapp2.RequestHandler):	 
	def post(self):
		user = users.get_current_user()
		mail=user.email()
		global type_user # holds the user type 
		mail_address = self.request.get("mail_address") #Request data from the POST request
		if mail_address!=mail:
			wrong_mail_template = jinja_environment.get_template('wrong_mail.html')
			self.response.write(wrong_mail_template.render())
		else:
			name = self.request.get("name")
			phone_no1 = self.request.get("phone_no1")
			phone_no2 = self.request.get("phone_no2")
			city = self.request.get("City")
			if type_user=='dogwalker':  # cheking if the user is a dogwalker or a dog owner 
				work_days = self.request.get_all("work_days")  #Request data from the POST request
				for i in range(len(work_days)):
					work_days[i]=str(work_days[i])
				payment_per_walk = self.request.get("price")
				breeds_handle = self.request.get_all("breed_handle")
				for i in range(len(breeds_handle)):
					breeds_handle[i]=str(breeds_handle[i])
				logging.info('breeds handle is %s'%breeds_handle)
				max_no_of_dogs_per_day = self.request.get("limit")
				web_user=web_users.DogWalker(name,mail_address,phone_no1,phone_no2,city,work_days,payment_per_walk,breeds_handle,max_no_of_dogs_per_day)
				web_user.insertToDb() #creating a dogwalker object and inserting it to the data base 
			else: 
				web_user=web_users.DogOwnerRegular(name,mail_address,phone_no1,phone_no2,city)
				web_user.insertToDb() #creating a dogowner object and inserting it to the data base 
			parameters_for_template = {'type_user': type_user}
			congrats = jinja_environment.get_template('congrats.html')
			self.response.write(congrats.render(parameters_for_template))
			

class CheckDogWalkers(webapp2.RequestHandler):
	def get(self):
		
		list_of_days=['Sunday','Monday','Tuesday','Wednsday','Thursday','Friday','Saturday']
		list_of_cities=['Tel-Aviv','Jerusalem','Haifa','Eilat','Bat-Yam','Netanya','Ramat-Hasharon','Zichron-Yaakov','Holon','Hadera','Afula','Netivot']
		list_of_dog_walkers=web_users.get_dog_walkers()
		list_of_dog_walkers=((walker[0].encode("ascii"),walker[1].encode("ascii"),walker[2].encode("ascii")) for walker in list_of_dog_walkers)
		parameters_for_template={'list_of_days': list_of_days,'list_of_cities': list_of_cities,'dog_walkers': list_of_dog_walkers}
		check_dogs = jinja_environment.get_template('filter_dog_walkers.html')
		self.response.write(check_dogs.render(parameters_for_template))

class SentCheckDogWalkers(webapp2.RequestHandler):
	def post(self):
		dogwalker=self.request.get('dogwalker')
		if dogwalker=='None':
			city = str(self.request.get("City"))
			days=self.request.get_all("work_days")
			for i in range(len(days)):
					days[i]=str(days[i])
			list_of_dog_walkers=web_users.get_dog_walkers(city=city,days=days)
			list_of_dog_walkers=list_of_dog_walkers[0]
			
			
			if not list_of_dog_walkers:
				woofpsi=jinja_environment.get_template('woofpsie.html')
				self.response.write(woofpsi.render())
			else:
				user_dogs = web_users.get_dogs_from_user()
				user_dogs=list((dog[0].encode("ascii") for dog in user_dogs))
				list_of_days=['Sunday','Monday','Tuesday','Wednsday','Thursday','Friday','Saturday']
				parameters_for_template={'list_of_days': list_of_days,'user_dogs': user_dogs,'dog_walkers': list_of_dog_walkers}
				register = jinja_environment.get_template('registerForm.html')
				self.response.write(register.render(parameters_for_template))

class AssignDogWalker(webapp2.RequestHandler):			
		def post(self):
			dog=self.request.get("user-selected_dog")
			day=self.request.get("day")
			dogwalker=self.request.get("dogwalker")
			logging.info("dog walker is {}".format(dogwalker))
			is_ok=web_users.is_register_valid(day,dogwalker)
			if is_ok:
				# register the dog walk in the database and navigate to the congrats page
				#web_users.register_walk()
				congrats = jinja_environment.get_template('congrats.html')
				self.response.write(congrats.render())
			else:
				woofpsi=jinja_environment.get_template('woofpsie.html')
				self.response.write(woofpsi.render())
				# dog walker is not avialable , navigate to not woofpsie page 
		

		
		
		
		
		
		
			
# -----------------------------------------
# class to logout from the google account
# and show the status aftewards
# Handles /logout 
# -----------------------------------------
class Logout(webapp2.RequestHandler):
    def get(self):

        logging.info('In Logout.get()')
        # if the user is logged in - we will perform log out
        user = users.get_current_user()

        if user:
            logging.info('The user is logged in - performing logout ')
            
            # force the user to logout and redirect him afterward to the home page
            self.redirect(users.create_logout_url('/'))

        else:
            logging.info('user is now not logged in ')
            logging.info('The user is logged out. There is nothing to do')
            logging.info('Redirecting to HomePage')
            self.redirect('/')

			
			
			
# --------------------------------------------------
# Routing
# --------
# /            - shows usage message
# /show_status - shows the status of the user - logged in or logged out
# /login       - performs login and then shows the status
# /logout      - performs log out and then shows the status
# --------------------------------------------------
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/logout', Logout),('/register', Register),('/login', Login),('/typeuser',SentType),
							   ('/sentRegistration',SentRegistration),('/dog_registration', SentDogInfo),('/register_dog', RegisterDog),
							   ('/check_dogwalkers',CheckDogWalkers),('/SentCheckDogWalkers',SentCheckDogWalkers),('/dogAssignedtoDogWalker',AssignDogWalker)],
                              debug=True)
