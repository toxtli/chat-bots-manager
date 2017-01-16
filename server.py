# python server.py
# curl http://localhost:8080/bot/twitter/twitter-config/msg/send?body=Hi

import sys
from ChatBot import ChatBot

def main(argv):
	chatbot = ChatBot(argv)
	chatbot.start()
	input('Press any key to exit.')

if __name__ == "__main__":
	argv = sys.argv[1:]
	main(argv)
