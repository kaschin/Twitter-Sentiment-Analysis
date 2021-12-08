import sys
import csv
import tweepy
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Enter Twitter API credentials here: 
Consumer_Key = "nAVj9mvFcoewA9rcDhIhnPfOY"
Consumer_Secret = "KICoP2C0oWHLDtkbciFKH32gCT0scJqbfUxTv2FbHj1Q3zDksl"
Access_Key = "1438843942980632580-eNGRp56B0fpo1to5oZDH0V2nafdbr3"
Access_Secret = "7JNsPBbpdJ2soCrqqlGF1xNe7XSKyYFCZdg76L9WIV4kI"

# Pulls and writes Tweets about current trending Topics to CSV
def scrape_viral_tweets():

	# Authenticate with Twitter credentials
	Auth = tweepy.OAuthHandler(Consumer_Key, Consumer_Secret)
	Auth.set_access_token(Access_Key, Access_Secret)
	api = tweepy.API(auth=Auth, retry_delay=450, retry_count=5)

	# Array to store different region codes
	WOEIDCodes = []
	# WOEID of San Francisco
	WOEIDCodes.append('2487956')
	# New York
	WOEIDCodes.append('2459115')
	# London
	WOEIDCodes.append('44418')
	# Toronto
	WOEIDCodes.append('4118')
	# Australia
	WOEIDCodes.append('23424748')

	# Create Array for storage to be written to CSV
	Tweets = []
	Tweets.append(["Username", "Tweet ID", "Tweet", "Favourites Count", "Retweet Count"])
	i=0
	for location in WOEIDCodes:
		trends = api.get_place_trends(id = location)
		for value in trends:
			for trend in value['trends']:
				i+=1
				print("Current Trend #" + str(i) + ": " + trend['name'])
				# Search for Tweets about Trend
				tweets = api.search_tweets(q=trend['name'], count=100, result_type='popular', lang='en') 
				# Append Tweet and details to container
				for tweet in tweets:
					tweeter = tweet._json['user']
					Tweets.append([tweeter['screen_name'], tweet._json['id_str'], tweet._json['text'], tweet._json['favorite_count'], tweet._json['retweet_count']])

	# Create CSV Outfile
	outfile = "Datasts/Viral_Tweets.csv"
	# Write to CSV File
	print("Writing to: " + str(outfile))
	with open(outfile, 'w+') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerows(Tweets)

# Main function
if __name__ == '__main__':
		scrape_viral_tweets()

