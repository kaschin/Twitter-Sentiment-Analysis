# Twitter Sentiment Analysis

A Sentiment Model that can be used to analysed the Sentiment of a series of Twitter Messages.

## Description

The intent of the project is to form an analysis of the Sentiment distribution of a series of Tweets. The Sentiment Model is trained to interpet Positive, Neutral and Negative sentiments but is restricted to only understanding words within the bounds of the provided training dataset. Scraping functions are provided to prepare datasets for the model to be tested on.

## Getting Started

#### Preparing Data (Optional)
The provided datasets can be used to test the Sentiment Model, or a custom dataset can be created with the following functions.
* User_Tweet_Scraper.py can be called with at least one argument to write to a/multiple CSV file(s) with Tweets pulled from the specified Twitter handle(s). Example terminal:
```
Python3 User_Tweet_Scraper.py TwittHandle1 TwitterHandle2 ... TwitterHandleN
```
* Viral_Tweet_Scraper.py can be used to pull the most popular Tweets of trending topics on Twitter within the most active regions. Example terminal:
```
Python3 Viral_Tweet_Scraper.py
```
If a custom dataset is used, modify line 136 of SentimentModel.py to contain the name of the new directory.
```
136   tweets_for_analysis = pandas.read_csv('custom_dataset.csv')
```
### Dependencies

* NLTK, Pandas, Tweepy

### Installing

* Project can be downloaded directly from Github with directories in place.

### Executing program

* Model can be built and tested with the following command:
```
Python3 SentimentModel.py 
```
## Authors

* Kayla Schinella 

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## Acknowledgments

* [awesome-readme](https://github.com/matiassingers/awesome-readme)
