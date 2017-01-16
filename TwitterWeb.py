import json
import time
import ConfigParser
from selenium import webdriver
from SeleniumHelper import SeleniumHelper

class TwitterWeb(SeleniumHelper):
	LOGIN_USER_VALUE = ''
	LOGIN_PASS_VALUE = ''
	TIMEOUT = 7

	DEBUG = False
	INITIAL_URL = 'https://mobile.twitter.com/login'
	WRITE_URL = 'https://mobile.twitter.com/compose/tweet'
	REPLY_URL = 'https://mobile.twitter.com/a/status/'
	# REPLY_URL = 'https://mobile.twitter.com/alcanzarlameta/reply/'
	SUBMIT_BUTTON = 'button[data-testid="tweet-button"]'

	INITIAL_MOBILE_URL = 'https://m.facebook.com/'
	SEARCH_LATEST_URL = 'https://www.facebook.com/search/latest/?q='
	ITEMS_CONTAINER = '#BrowseResultsContainer'
	# ITEMS_COMMENTABLE = '.commentable_item'
	ITEMS_COMMENTABLE = '.comment_link'
	ITEM_ID = 'input[name=ft_ent_identifier]'
	ITEM_TEXT = '.text_exposed_root'
	ITEM_CONTENT = '.userContent > p'
	LOGIN_USER_PATH = '[name="session[username_or_email]"]'
	LOGIN_PASS_PATH = '#session\\[password\\]'
	LOGIN_SUBMIT_PATH = '#loginbutton > input[type="submit"]'
	SEARCH_BAR_PATH = 'input.inputtext'
	SEARCH_URL = 'https://www.facebook.com/search/str/'
	SEARCH_PEOPLE_URL = '/keywords_users?ref=top_filter'
	SEARCH_WORK_STRING = 'People who work at '
	USER_LIST_CONTAINER_PATH = '#BrowseResultsContainer'
	USER_NAME_PATH = 'div > div > div > div > div.clearfix > div._gll > a > div > div > div'
	USER_POSITION_PATH = 'div > div > div > div > div._glm > div'
	USER_DESCRIPTION_PATH = 'div > div > div > div > div._glo > div'
	USER_IMAGE_PATH = 'div > div > a > img'
	USER_URL_PATH = 'div > div > a'
	TEXTBOX_COMMENT = '#composerInput'
	SUBMIT_COMMENT_PATH = 'input[type="submit"]'
	POST_COMMENT_CONTAINER = '.UFIList'
	POST_COMMENT_BLOCKS = '.UFICommentContent'
	POST_COMMENT_NAME = '.UFICommentActorName'
	POST_COMMENT_TEXT = '.UFICommentBody'
	REPLY_BUTTON = '[data-testid="reply"]'
	REPLY_SEND_BUTTON = '[data-testid="tweet-button"]'

	MESSAGES_LIST = '.webMessengerMessageGroup'
	MESSAGE_FROM = 'div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > strong:nth-child(1) > a:nth-child(1)'
	MESSAGE_TEXT = 'div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'
	MESSAGE_DATE = 'div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > abbr:nth-child(3)'

	MESSAGE_URL = 'https://www.facebook.com/messages/'
	MESSAGE_BUTTON = '#pagelet_timeline_profile_actions > div:nth-child(2) > a:nth-child(2)'
	MESSAGE_TEXTAREA = 'textarea'

	data = {}
	baseUrl = ''
	argv = None
	client = None

	def bot_exec(self, section, action, params):
		exit = {'status': 'OK', 'data': 'test'}
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
		elif section == 'search':
			if action == 'posts':
				if 'q' in params:
					exit['data'] = self.search_posts(params['q'])
				else:
					exit['data'] = json.dumps(params)
		elif section == 'post':
			if action == 'send':
				if 'body' in params and 'to' in params:
					exit['data'] = self.post_message(params['to'], params['body'])
				else:
					exit['data'] = json.dumps(params)
			elif action == 'read':
				if 'to' in params:
					exit['data'] = self.post_read_messages(params['to'])
				else:
					exit['data'] = json.dumps(params)
		elif section == 'screen':
			if action == 'shot':
				self.saveScreenshot('screenshot4.png')
		elif section == 'get':
			print "TEST01"
			if action == 'fbid':
				print "TEST02"
				if 'id' in params:
					print "TEST03"
					newId = self.get_real_id(params['id'])
					exit = {'status':'OK', 'data':{'id': newId}}
		if exit['data'] != 'OK':
			exit['status'] = 'ERROR'
		exit['timestamp'] = str(time.time())
		return exit

	def login(self):
		self.loadPage(self.INITIAL_URL)
		userInput = self.waitShowElement(self.LOGIN_USER_PATH)
		userInput.send_keys(self.LOGIN_USER_VALUE)
		passInput = self.getElement(self.LOGIN_PASS_PATH)
		passInput.send_keys(self.LOGIN_PASS_VALUE)
		self.submitForm(passInput)

	def close(self):
		self.driver.quit()

	def start(self):
		print 'Logging in'
		self.login()
		self.saveScreenshot()

	def getInfo(self, url):
		command = 'linkedin-scraper ' + url
		try:
			output = subprocess.check_output(command.split())
			userInfo = json.loads(output)
		except:
			userInfo = {}
		return userInfo

	def post_read_messages(self, to):
		exit = []
		self.loadPage(self.INITIAL_URL + to)
		container = self.waitShowElement(self.POST_COMMENT_CONTAINER)
		items = self.getElements(self.POST_COMMENT_BLOCKS)
		for item in items:
			name = self.getElementFromValue(item, self.POST_COMMENT_NAME)
			text = self.getElementFromValue(item, self.POST_COMMENT_TEXT)
			exit.append({'name': name, 'text': text})
		return exit


	def post_message(self, to, body):
		self.loadPage(self.INITIAL_MOBILE_URL + to)
		textbox = self.waitAndWrite(self.TEXTBOX_COMMENT, body)
		self.pressEnter(textbox)
		return 'OK'


	def get_real_id(self, id):
		print "TEST04"
		return self.get_user_id(self.INITIAL_URL + id)


	def send_message(self, body, to=None, image=None):
		try:
			message = body
			if to:
				message = to + " " + message
			url = self.WRITE_URL
			print 'Loading message page ...'
			self.loadPage(url)
			print 'Page loaded'
			print 'Typing'
			if self.DEBUG:
				self.saveScreenshot('screenshot2.png');
			textarea = self.waitShowElement(self.MESSAGE_TEXTAREA)
			textarea.send_keys(message)
			# textarea.send_keys(Keys.TAB)
			# textarea.send_keys(Keys.RETURN)
			
			button = self.getElement(self.SUBMIT_BUTTON)
			self.click(button)
			print 'Sent'
			# textarea.send_keys('\r\n')
			# self.saveScreenshot('screenshot3.png');
			return 'OK'
		except Exception as e:
			print "Message not sent"
			print sys.exc_info()
			return str(e)

	def reply_message(self, body, id, to=None, image=None):
		try:
			message = body
			if to:
				message = to + " " + message
			url = self.REPLY_URL + id
			print 'Loading message page ...'
			self.loadPage(url)
			print 'Page loaded'
			print 'Typing'
			if self.DEBUG:
				self.saveScreenshot('screenshot2.png');
			button = self.waitShowElement(self.REPLY_BUTTON)
			self.click(button)
			textarea = self.waitShowElement(self.MESSAGE_TEXTAREA)
			textarea.send_keys(message)
			# textarea.send_keys(Keys.TAB)
			# textarea.send_keys(Keys.RETURN)
			# textarea.submit()
			button = self.getElement(self.REPLY_SEND_BUTTON)
			self.click(button)
			print 'Sent'
			# textarea.send_keys('\r\n')
			# self.saveScreenshot('screenshot3.png');
			return 'OK'
		except Exception as e:
			print "Message not sent"
			print sys.exc_info()
			return str(e)

	def read_messages(self, to):
		exit = []
		url = self.MESSAGE_URL + to
		self.loadPage(url)
		textarea = self.waitShowElement(self.MESSAGE_TEXTAREA)
		messages = self.getElements(self.MESSAGES_LIST)
		for message in messages:
			values = {}
			values['from'] = self.getElementFromValue(message, self.MESSAGE_FROM)
			values['text'] = self.getElementFromValue(message, self.MESSAGE_TEXT)
			values['date'] = self.getElementFromValue(message, self.MESSAGE_DATE)
			exit.append(values)
		return exit

	def search_posts(self, query):
		exit = []
		self.loadPage(self.SEARCH_LATEST_URL + query)
		container = self.waitShowElement(self.ITEMS_CONTAINER)
		items = self.getElements(self.ITEMS_COMMENTABLE)
		print len(items)
		for item in items:
			print 'FOUND'
			form = self.getParentLevels(item, 9)
			idValue = self.getElementFromAttribute(form, self.ITEM_ID, 'value')
			text = self.getElementFromValue(form, self.ITEM_CONTENT)
			exit.append({'id': idValue, 'text': text})
		return exit

	def get_user_id(self, url):
		print "TEST05"
		self.loadPage(url)
		html = self.driver.page_source
		idVal = html.split('content="fb://profile/')[1].split('"')[0]
		return idVal

	def saveToFile(self, fileName):
		file_ = open(fileName, 'w')
		content = json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))
		file_.write(content)
		file_.close()

	def __init__(self, filename):
		config = ConfigParser.ConfigParser()
		config.read(filename)
		self.LOGIN_USER_VALUE = config.get('credentials', 'login_user_value')
		self.LOGIN_PASS_VALUE = config.get('credentials', 'login_pass_value')
		# self.client = fbchat.Client(self.LOGIN_USER_VALUE, self.LOGIN_PASS_VALUE)
		profile = webdriver.FirefoxProfile()
		profile.set_preference("javascript.enabled", False)
		self.driver = webdriver.Firefox(profile)
		# self.driver = webdriver.PhantomJS()
		# self.driver = webdriver.Chrome('./chromedriver')
		self.driver.set_page_load_timeout(self.TIMEOUT)