import csv
import pandas
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
import re, string
from nltk.corpus import stopwords
from nltk import FreqDist
import random
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize

# Remove noise from Twitter message
def RemoveNoise(tweet_tokens):

    clean_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        # Delete any hyperlinks
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        # Delete any tags/mentions (@)
        token = re.sub('(@[A-Za-z0-9_]+)','', token)

        # Determine whether the tag of token is noun, verb or adjective
        if tag.startswith('NN'): # Noun (singular)
            pos = 'n'
        elif tag.startswith('VB'): # Verb (ask)
            pos = 'v'
        else: # Adjective (large)
            pos = 'a'

        # Reduce token to canonical value through lemmatisation
        lemmatiser = WordNetLemmatizer()
        token = lemmatiser.lemmatize(token, pos)

        # Define Stop Words - words that indiciate little meaning
        stop_words = stopwords.words('english')

        # Check if token is not empty, punctuation, or a stop word
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            clean_tokens.append(token.lower()) # Reduce to lower case and append

    return clean_tokens

# Determine word density (calculating frequency of a word with a particular sentiment)
def get_all_words(clean_tokens_list):
    for tokens in clean_tokens_list:
        for token in tokens:
            yield token # Create generator

# Convert format of clean data into a dictionary
def get_tweets_for_model(clean_tokens_list):
    for tweet_tokens in clean_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def Build_Model():

    # Grab data from CSV files to create dataframe for modelling
    df = pandas.read_csv('Training_Tweets.csv')
    Tweets_df = pandas.DataFrame(df, columns = df.columns) # Convert to Pandas Dataframe

    positive_tweet_tokens = pandas.DataFrame(columns = df.columns)
    negative_tweet_tokens = pandas.DataFrame(columns = df.columns)
    neutral_tweet_tokens = pandas.DataFrame(columns = df.columns)

    # Divide data by given Sentiment
    for i in range(len(Tweets_df)):
        Sentiment = Tweets_df["airline_sentiment"].iloc[i]
        if Sentiment == "positive":
            positive_tweet_tokens = positive_tweet_tokens.append(Tweets_df.iloc[i]);
        elif Sentiment == "negative":
            negative_tweet_tokens = negative_tweet_tokens.append(Tweets_df.iloc[i]);
        elif Sentiment == "neutral":
            neutral_tweet_tokens = neutral_tweet_tokens.append(Tweets_df.iloc[i]);

    # Initialise clean token sentiment containers
    positive_clean_tokens_list = []
    negative_clean_tokens_list = []
    neutral_clean_tokens_list = []

    for message in positive_tweet_tokens['text']:
    	tokens = message.split()
    	positive_clean_tokens_list.append(RemoveNoise(tokens))

    for message in negative_tweet_tokens['text']:
    	tokens = message.split()
    	negative_clean_tokens_list.append(RemoveNoise(tokens))

    for message in neutral_tweet_tokens['text']:
    	tokens = message.split()
    	neutral_clean_tokens_list.append(RemoveNoise(tokens))

    # Find most common positive, neutral and negative tokens
    # all_pos_words = get_all_words(positive_clean_tokens_list)
    # all_neg_words = get_all_words(negative_clean_tokens_list)
    # all_neu_words = get_all_words(neutral_clean_tokens_list)

    # freq_dist_pos = FreqDist(all_pos_words)
    # freq_dist_neg = FreqDist(all_neg_words)
    # freq_dist_neu = FreqDist(all_neu_words)

    positive_tokens_for_model = get_tweets_for_model(positive_clean_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_clean_tokens_list)
    neutral_tokens_for_model = get_tweets_for_model(neutral_clean_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    neutral_dataset = [(tweet_dict, "Neutral")
                         for tweet_dict in neutral_tokens_for_model]

    # Append positive, negative and neutral dataset to one
    dataset = positive_dataset + negative_dataset + neutral_dataset
    random.shuffle(dataset) # Shuffle the values such that model can be divided
    DF_length = len(dataset)
    train_data = dataset[:round(DF_length * .90)] # Implement 90% of the data for training
    test_data = dataset[round(DF_length * .90):] # Implement 10% of the data for testing

    classifier = NaiveBayesClassifier.train(train_data)

    # Output information about Model
    print("Accuracy is: ", classify.accuracy(classifier, test_data))
    print(classifier.show_most_informative_features(10))

    return classifier

# Main function
if __name__ == '__main__':

    # Implement a CSV of Twitter messages to be tested on
    Viral_Tweets = pandas.read_csv('1future_tweets.csv')
    Viral_Tweets = pandas.DataFrame(Viral_Tweets, columns = Viral_Tweets.columns)
    DF_length = float(len(Viral_Tweets))

    # Input a list of Custom Tweets here to be tested
    custom_tweets = ["The wall is white", "That is ugly", "Awesome!"]

    # Initialise sentiment count
    PosSent = NegSent = NeuSent = 0.00

    # Build Model
    classifier = Build_Model()

    # Analyse Viral Tweets from dataset
    for tweet in Viral_Tweets['Tweet']:
        custom_tokens = RemoveNoise(word_tokenize(tweet))
        sentiment = (classifier.classify(dict([token, True] for token in custom_tokens)))
        if (sentiment == "Positive"):
            PosSent += 1
        elif (sentiment == "Negative"):
            NegSent += 1
        elif (sentiment == "Neutral"):
            NeuSent += 1

    print("Positive Sentiment distribution: " + str(float(PosSent/DF_length)))
    print("Neutral Sentiment distribution: ", str(float(NeuSent/DF_length)))
    print("Negative Sentiment distribution: ", str(float(NegSent/DF_length)))

    # Analyse Custom Tweets
    for custom_tweet in custom_tweets:
     	custom_tokens = RemoveNoise(word_tokenize(custom_tweet))

     	print("Tweet Message: " + custom_tweet + "\n" + "Sentiment is: " + classifier.classify(dict([token, True] for token in custom_tokens)))










