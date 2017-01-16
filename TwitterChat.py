import sys
import json
import time
import tweepy
import ConfigParser

class TwitterChat:
	screen_name = ""
	consumer_key = ""
	consumer_secret = ""
	access_token = ""
	access_token_secret = ""
	configured = False
	language = 'en'
	max_tweets = 100
	auth = None
	api = None
	user = None
	data = {}

	def bot_exec(self, section, action, params):
		exit = {'status':'OK', 'data':'test'}
		if section == 'msg':
			if action == 'send':
				if 'body' in params:
					to = None
					if 'to' in params:
						to = params['to']
					image = None
					if 'image' in params:
						image = params['image']
					exit['data'] = self.send_message(params['body'], to, image)
				else:
					exit['data'] = json.dumps(params)
			elif action == 'reply':
				if 'body' in params and 'id' in params:
					to = None
					if 'to' in params:
						to = params['to']
					image = None
					if 'image' in params:
						image = params['image']
					exit['data'] = self.reply_message(params['body'], params['id'], to, image)
				else:
					exit['data'] = json.dumps(params)
			elif action == 'read':
				if 'to' in params:
					exit['data'] = self.read_messages(params['to'])
				else:
					exit['data'] = self.read_all_messages()
		if exit['data'] != 'OK':
			exit['status'] = 'ERROR'
		exit['timestamp'] = str(time.time())
		return exit

	def send_message(self, body, to=None, image=None):
		print "Sending message"
		message = body
		if to:
			message = to + " " + message
		try:
			if image:
				self.api.update_with_media(status=message, filename=image)
			else:
				self.api.update_status(status=message)
			print "Message sent"
			return 'OK'
		except Exception as e:
			print "Message not sent"
			print sys.exc_info()
			return str(e)

	def reply_message(self, body, id, to=None, image=None):
		print "Reply message"
		message = body
		if to:
			message = to + " " + message
		try:
			if image:
				self.api.update_with_media(status=message, filename=image, in_reply_to_status=id)
			else:
				print "Using reply"
				self.api.update_status(status=message, in_reply_to_status=id)
			print "Message replied"
			return 'OK'
		except Exception as e:
			print "Message not sent"
			print sys.exc_info()
			return str(e)

	def read_messages(self, to):
		exit = []
		searched_tweets = [status for status in tweepy.Cursor(self.api.search, q=to, lang=self.language).items(self.max_tweets)]
		for elem in searched_tweets:
			exit.append({'user_tweets':elem.user.id,'screen_name':elem.user.screen_name,'description':elem.user.description,'tweet_message':elem.text,'created_date':str(elem.created_at)})
		return exit

	def close(self):
		self.auth = None
		self.api = None

	def login(self):
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(self.auth)
		self.user = self.api.get_user(self.screen_name)
		return True

	def start(self):
		if self.login():
			print 'Logged in'
		else:
			print 'Not logged in'

	def __init__(self, filename):
		config = ConfigParser.ConfigParser()
		config.read(filename)
		self.screen_name = config.get('credentials', 'screen_name')
		self.consumer_key = config.get('credentials', 'consumer_key')
		self.consumer_secret = config.get('credentials', 'consumer_secret')
		self.access_token = config.get('credentials', 'access_token')
		self.access_token_secret = config.get('credentials', 'access_token_secret')