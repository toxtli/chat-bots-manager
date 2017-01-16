import web
import json
import getopt
import threading
from TwitterChat import TwitterChat
from TwitterWeb import TwitterWeb
from FacebookChat import FacebookChat
from LinkedinChat import LinkedinChat

class ChatBot:
	port = 8080
	argv = None
	urls = (
	    '/', 'bot',
	    '/bot', 'bot_status_all',
	    '/bot/(.*)', 'bot_commands'
	)
	instances = {}

	class bot:        
	    def GET(self):
	        raise web.seeother('/static/index.html')

	class bot_status_all:        
	    def GET(self):
	        output = {"data":"null"}
	        exit = json.dumps(output)
	        return exit

	class bot_commands:
		configPath = './'
		instances = {}

		def GET(self, data):
			print 'New request'
			exit = {'status':'error', 'data':'Invalid arguments'}
			arrData = data.split('/')
			if len(arrData) >= 4:
				platform = arrData[0]
				instance = arrData[1]
				section = arrData[2]
				action = arrData[3]
				configFile = self.configPath + instance
				exit = {'status':'error', 'data': 'Invalid platform'}
				link = None
				if platform == 'twitterapi':
					if not instance in self.instances:
						print 'Creating instance'
						self.instances[instance] = TwitterChat(configFile)
						self.instances[instance].start()
				elif platform == 'twitter':
					if not instance in self.instances:
						print 'Creating instance'
						self.instances[instance] = TwitterWeb(configFile)
						self.instances[instance].start()
				elif platform == 'facebook':
					if not instance in self.instances:
						print 'Creating instance'
						self.instances[instance] = FacebookChat(configFile)
						self.instances[instance].start()
				elif platform == 'linkedin':
					if not instance in self.instances:
						print 'Creating instance'
						self.instances[instance] = LinkedinChat(configFile)
						self.instances[instance].start()
				if instance in self.instances:
					print 'Executing instance'
					exit = self.instances[instance].bot_exec(section, action, web.input())
			return json.dumps(exit)

	def start(self):
		thread = threading.Thread(target=self.run)
		thread.setDaemon(True)
		thread.start()
		print 'Server is ready to serve'

	def run(self):
		port = 8080
		app = web.application(self.urls, {
			'bot':self.bot, 
			'bot_commands':self.bot_commands, 
			'bot_status_all':self.bot_status_all})
		web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", self.port))

	def __init__(self, argv):
		self.argv = argv
		opts, args = getopt.getopt(self.argv, "c:p:")
		if opts:
			for o, a in opts:
				if o == "-p":
					self.port = int(a)