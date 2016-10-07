import sys
from ChatBot import ChatBot

def main(argv):
	chatbot = ChatBot(argv)
	chatbot.start()
	input('Press any key to exit.')

if __name__ == "__main__":
	argv = sys.argv[1:]
	main(argv)
