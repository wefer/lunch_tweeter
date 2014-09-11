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

def tweet(conf, info):
	"""
	Tweet messages after splitting them into chunks if necessary
	"""
	name = info[0]
	day = info[1]
	message = info[2]
	spacer = '-' * 30
	header = "%s: %s\n%s" % (name, day, spacer)

	# Get API-object 
	api = get_twitter_auth(conf)
	
	if len(message) < 140:
		#post message
		api.statuses.update(status=message)

	else:
		#split message into chunks
		short_messages = []
		paragraphs = message.split('\n')
		word = ""
		for item in paragraphs:

			
                        if len(word + '\n' + item) < 140:

                                word = word + '\n' + item
                        else:
                                short_messages.append(word)
                                word = item
 
                if word not in short_messages:

                          short_messages.append(word)

		for item in short_messages[::-1]:
			api.statuses.update(status=item)

		api.statuses.update(status=header)

	return 0
