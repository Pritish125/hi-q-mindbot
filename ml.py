import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

def get_most_similar_sentiment(user_input, data_file='more.csv', nrows=1000):
    # Load the dataset
    data = pd.read_csv(data_file, nrows=nrows)
    
    # Initialize the VADER sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Perform sentiment analysis on the patient responses
    sentiments = []
    for response in data['conversations']:
        sentiment_score = sid.polarity_scores(response)
        sentiments.append(sentiment_score['compound'])

    # Perform sentiment analysis on the user input
    user_sentiment = sid.polarity_scores(user_input)
    user_sentiment_compound = user_sentiment['compound']

    # Compare the user's sentiment with the sentiments in the dataset
    # Find the response with the most similar sentiment
    most_similar_idx = min(range(len(sentiments)), key=lambda i: abs(sentiments[i] - user_sentiment_compound))

    most_similar_sentiment = sentiments[most_similar_idx]

    return most_similar_sentiment

# Test the function with user input
user_input = "I'm feeling very good"
most_similar_sentiment = get_most_similar_sentiment(user_input)
print("Most similar sentiment score based on VADER analysis:", most_similar_sentiment)
