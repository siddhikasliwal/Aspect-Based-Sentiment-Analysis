import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

df = pd.read_csv('APPLE_iPhone_SE.csv')
df_new = pd.read_csv('new_df.csv')
# Download the 'vader_lexicon' resource
nltk.download('vader_lexicon')

# Perform sentiment analysis on the 'Reviews' column
# Initialize SentimentIntensityAnalyzer
sentiments = SentimentIntensityAnalyzer()

# Perform sentiment analysis on the 'Reviews' column
positive_scores = []
negative_scores = []
neutral_scores = []

for review in df_new["Reviews"]:
    if not pd.isna(review):  # Check for NaN values
        sentiment_scores = sentiments.polarity_scores(review.encode("utf-8").decode("utf-8"))
        positive_scores.append(sentiment_scores["pos"])
        negative_scores.append(sentiment_scores["neg"])
        neutral_scores.append(sentiment_scores["neu"])
    else:
        # Handle NaN values with neutral sentiment
        positive_scores.append(0)
        negative_scores.append(0)
        neutral_scores.append(1)

df_new["Positive"] = positive_scores
df_new["Negative"] = negative_scores
df_new["Neutral"] = neutral_scores

# Select and reorder columns to keep only 'Reviews', 'Positive', 'Negative', and 'Neutral'
df_new = df_new[["Reviews", "Positive", "Negative", "Neutral"]]

# Calculate the total sum of positive, negative, and neutral sentiment scores
x = sum(df_new["Positive"])
y = sum(df_new["Negative"])
z = sum(df_new["Neutral"])

# Define a function to determine the overall sentiment score based on the sums
def sentiment_score(a, b, c):
    if (a>b) and (a>c):
        print("Positive 😊 ")
    elif (b>a) and (b>c):
        print("Negative 😠 ")
    else:
        print("Neutral 🙂 ")

sentiment_score(x, y, z)

# Printing the respective scores
print("Positive: ", x)
print("Negative: ", y)
print("Neutral: ", z)

# Count the number of occurrences of each unique rating in the 'Ratings' column.
ratings = df['Ratings'].value_counts()

# Extract the unique ratings and their respective counts
numbers = ratings.index
quantity = ratings.values

# List of aspects for sentiment analysis
aspects = ['battery backup', 'value for money', 'features', 'camera', 'battery',
    'display']

# Initialize SentimentIntensityAnalyzer
sentiments = SentimentIntensityAnalyzer()

# Create dictionaries to store sentiment scores and review counts for each aspect
aspect_sentiments = {aspect: [] for aspect in aspects}
aspect_review_counts = {aspect: 0 for aspect in aspects}

# Iterate through the reviews and perform aspect-based sentiment analysis
for review in df['Reviews']:

   # Convert the review text to lowercase for consistent matching
    review = review.lower()

    # Perform sentiment analysis on the review using the 'sentiments' analyzer
    sentiment_scores = sentiments.polarity_scores(review)

    # Iterate through the aspects you want to analyze
    for aspect in aspects:

      # Check if the aspect keyword is present in the review text
        if aspect in review:

           #Append the sentiment scores of the review
            aspect_sentiments[aspect].append(sentiment_scores)

            # Increment the review count for the aspect in aspect_review_counts
            aspect_review_counts[aspect] += 1


# Calculate average sentiment scores for each aspect

# Create an empty dictionary to store the average sentiment scores for each aspect
average_aspect_sentiments = {}

# Iterate over each aspect and its corresponding sentiment scores in the aspect_sentiments dictionary
for aspect, scores in aspect_sentiments.items():

  # Check if there are sentiment scores available for the aspect (avoid division by zero)
    if len(scores) > 0:
        average_scores = {
            'positive': sum(score['pos'] for score in scores) / len(scores),
            'neutral': sum(score['neu'] for score in scores) / len(scores),
            'negative': sum(score['neg'] for score in scores) / len(scores),
        }
        average_aspect_sentiments[aspect] = average_scores

# Iterate over each aspect and its corresponding sentiment scores in the dictionary
for aspect, scores in average_aspect_sentiments.items():
    print(f"Aspect: {aspect}")
    print(f"Positive: {scores['positive']:.2f}")
    print(f"Neutral: {scores['neutral']:.2f}")
    print(f"Negative: {scores['negative']:.2f}")
    print()
