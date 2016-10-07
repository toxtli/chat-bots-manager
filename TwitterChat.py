import json
import time
import tweepy
import ConfigParser

class TwitterChat:
	screen_name = "YourFriendlyBot"
	consumer_key = "6y7sRr5UsRbcqCy3e0H17cPYb"
	consumer_secret = "bJS0GKhX4O5BBWXp7L8bLG014lUd8VQQXZYqmVxjMxpFyEs5po"
	access_token = "4777368076-wr4qyFoVVjS67Zxkn94Bsye94I8YlfiKCkWN3F1"
	access_token_secret = "SS3gqbZ7ESA9dtSolZxc4DoixKh7AGCGU1ZFyIaumZoHZ"
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
				if 'body' in params and 'to' in params:
					image = None
					if 'image' in params:
						image = params['image']
					exit['status'] = self.send_message(params['body'], params['to'], image)
				else:
					exit['data'] = json.dumps(params)
			elif action == 'read':
				if 'to' in params:
					exit['data'] = self.read_messages(params['to'])
				else:
					exit['data'] = self.read_all_messages()
		exit['timestamp'] = str(time.time())
		return exit

	def send_message(self, body, to, image=None):
		print "Sending message"
		message = to + " " + body
		try:
			if image:
				self.api.update_with_media(status=message,filename=image)
			else:
				self.api.update_status(status=message)
			print "Message sent"
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