#!/usr/bin/python

import twitter
import yaml

def get_twitter_auth(config_file):
	"""
	Create twitter api instance
	"""
	with open(config_file) as f:
		api_params = yaml.load(f)
		token = api_params['token']
		token_key = api_params['token_key']
		con_secret = api_params['con_secret']
		con_secret_key = api_params['con_secret_key']

	api = twitter.Twitter(auth=twitter.OAuth(token,
		token_key,
		con_secret,
		con_secret_key)) 
	
	return api

def tweet(conf, user, message):
	"""
	Tweet messages after splitting them into chunks if necessary
	"""
	# Get API-object 
	api = get_twitter_auth(conf)
	
	if len(message) < 140:
		#post message
		api.direct_messages.new(user=user, text=message)

	else:
		#split message into chunks
		short_messages = []
		paragraphs = message.split('\n')
		word = ""
		for item in paragraphs:
			if len(word+item) < 140:
				word += item

			elif paragraphs.index(item) == len(paragraphs) - 1:
				short_messages.append(word)

			else:
				short_messages.append(word)
				word = item

		for item im short_messages[::-1]:
			api.direct_messages.new(user=user, text=item)

	return 0
