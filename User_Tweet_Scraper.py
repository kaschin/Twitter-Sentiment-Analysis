import sys
import csv
import tweepy

# Enter Twitter API credentials here: 
Consumer_Key = "nAVj9mvFcoewA9rcDhIhnPfOY"
Consumer_Secret = "KICoP2C0oWHLDtkbciFKH32gCT0scJqbfUxTv2FbHj1Q3zDksl"
Access_Key = "1438843942980632580-eNGRp56B0fpo1to5oZDH0V2nafdbr3"
Access_Secret = "7JNsPBbpdJ2soCrqqlGF1xNe7XSKyYFCZdg76L9WIV4kI"

# Get Tweets of a User by Twitter Handle
def scrape_tweets(username):

	# Authenticate with Twitter credentials
	Auth = tweepy.OAuthHandler(Consumer_Key, Consumer_Secret)
	Auth.set_access_token(Access_Key, Access_Secret)
	api = tweepy.API(Auth)

	# Set quantity of Tweets to be pulled
	tweet_quantity = 1

	# Intialise container for Tweets
	Tweets = []
	Tweets.append(["Username", "Tweet ID", "Creation Date", "Tweet"]) # Set column names

	# Append Twitter message and other information
	for tweet in tweepy.Cursor(api.user_timeline, screen_name = username).items(tweet_quantity):
		Tweets.append([username, tweet.id_str, tweet.created_at, tweet.text])

	# Create new CSV file
	outfile = "Datasets/" + username + "_Tweets.csv"

	# Write to CSV file
	print("Writing to: " + str(outfile))
	with open(outfile, 'w+') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerows(Tweets)

# Main function
if __name__ == '__main__':

	# Get tweets for username(s) passed at command line
	if len(sys.argv) >= 2:
		for i in range(1, len(sys.argv)):
			scrape_tweets(sys.argv[i])
	else:
		print("Error! Enter at least one username.")
