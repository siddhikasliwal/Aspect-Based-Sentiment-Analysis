from flask.templating import render_template
from flask import Flask
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
import plotly.express as px

template_folder = r"E:\sp_project\templates"

app = Flask(__name__, template_folder=template_folder)


def overview(df_new):
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

    # Calculate the total sum of positive, negative, and neutral sentiment scores
    x = sum(df_new["Positive"])
    y = sum(df_new["Negative"])
    z = sum(df_new["Neutral"])
    dic = {}
    dic["Positive"] = x
    dic["Negative"] = y
    dic["Neutral"] = z

    # Define a function to determine the overall sentiment score based on the sums
    def sentiment_score(a, b, c):
        if (a > b) and (a > c):
            print("Positive 😊 ")
            return "Positive 😊 "
        elif (b > a) and (b > c):
            print("Negative 😠 ")
            return "Negative 😠"
        else:
            print("Neutral 🙂 ")
            return "Neutral 🙂 "

    return sentiment_score(x, y, z), dic

def features(df_new, df):
    ratings = df['Ratings'].value_counts()
    # Extract the unique ratings and their respective counts
    numbers = ratings.index
    quantity = ratings.values

    # List of aspects for  n analysis
    aspects = ['battery backup', 'camera', 'features','battery','value for money']
    # Initialize SentimentIntensityAnalyzer
    sentiments = SentimentIntensityAnalyzer()

    # Create dictionaries to store sentiment scores and review counts for each aspect
    aspect_sentiments = {aspect: [] for aspect in aspects}
    aspect_review_counts = {aspect: 0 for aspect in aspects}

    # Iterate through the reviews and perform aspect-based sentiment analysis
    for review in df['Reviews']:
        if not pd.isna(review):
        # Convert the review text to lowercase for consistent matching
            review = review.lower()
        # Perform sentiment analysis on the review using the 'sentiments' analyzer
            sentiment_scores = sentiments.polarity_scores(review)
        # Iterate through the aspects you want to analyze
            for aspect in aspects:
            # Check if the aspect keyword is present in the review text
                if aspect in review:
                # Append the sentiment scores of the review
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
                'positive': round(sum(score['pos'] for score in scores) / len(scores), 2),
                'neutral': round(sum(score['neu'] for score in scores) / len(scores), 2),
                'negative': round(sum(score['neg'] for score in scores) / len(scores), 2),
            }
            average_aspect_sentiments[aspect] = average_scores
    return average_aspect_sentiments


@app.route('/')
def project():
    return render_template('index.html')


@app.route('/products')
def index():
    return render_template('products.html')


@app.route('/applese')
def applese():
    df = pd.read_csv('APPLE_iPhone_SE.csv')
    df_new = pd.read_csv('new_df.csv')
    maxi, dic = overview(df)
    aspect = features(df_new, df)  
    pos_score = dic["Positive"]
    neg_score = dic["Negative"]
    neu_score = dic["Neutral"]

    # Convert the scores to percentages with 2 decimal places\\\\
    pos_batterybackup = f"{aspect['battery backup']['positive'] * 100:.2f}%"
    neu_batterybackup = f"{aspect['battery backup']['neutral'] * 100:.2f}%"
    neg_batterybackup = f"{aspect['battery backup']['negative'] * 100:.2f}%"

    pos_camera = f"{aspect['camera']['positive'] * 100:.2f}%"
    neu_camera = f"{aspect['camera']['neutral'] * 100:.2f}%"
    neg_camera = f"{aspect['camera']['negative'] * 100:.2f}%"

    pos_features = f"{aspect['features']['positive'] * 100:.2f}%"
    neu_features = f"{aspect['features']['neutral'] * 100:.2f}%"
    neg_features = f"{aspect['features']['negative'] * 100:.2f}%"

    pos_battery = f"{aspect['battery']['positive'] * 100:.2f}%"
    neu_battery = f"{aspect['battery']['neutral'] * 100:.2f}%"
    neg_battery = f"{aspect['battery']['negative'] * 100:.2f}%"

    pos_value = f"{aspect['value for money']['positive'] * 100:.2f}%"
    neu_value = f"{aspect['value for money']['neutral'] * 100:.2f}%"
    neg_value = f"{aspect['value for money']['negative'] * 100:.2f}%"


    ratings = df['Ratings'].value_counts()
    numbers = ratings.index
    quantity = ratings.values
    labels = [f"Ratings {num}" for num in numbers]
    fig = px.pie(values=quantity, names=numbers, hole=0.5)
    div = fig.to_html(full_html=False)

    
    return render_template('Apple_SE.html', maxi=maxi, pos_score=pos_score, neg_score=neg_score,
                           neu_score=neu_score, pos_batterybackup=pos_batterybackup, 
                           neu_batterybackup=neu_batterybackup, 
                           neg_batterybackup=neg_batterybackup, 
                           pos_camera=pos_camera, 
                           neu_camera=neu_camera, 
                           neg_camera=neg_camera,
                           pos_features=pos_features, 
                           neu_features=neu_features, 
                           neg_features=neg_features,
                           pos_battery=pos_battery, 
                           neu_battery=neu_battery, 
                           neg_battery=neg_battery,
                           pos_value=pos_value, 
                           neu_value=neu_value, 
                           neg_value=neg_value,
                           plot_div=div)



@app.route('/samsungs5')
def samsungs5():
    df1 = pd.read_csv('Samsung G900F Galaxy S5.csv')
    df_new1 = pd.read_csv('new_df1.csv')
    maxi, dic = overview(df1)
    aspect = features(df_new1, df1)  
    pos_score = dic["Positive"]
    neg_score = dic["Negative"]
    neu_score = dic["Neutral"]
    # Convert the scores to percentages with 2 decimal places\\\\
    pos_batterybackup = f"{aspect['battery backup']['positive'] * 100:.2f}%"
    neu_batterybackup = f"{aspect['battery backup']['neutral'] * 100:.2f}%"
    neg_batterybackup = f"{aspect['battery backup']['negative'] * 100:.2f}%"

    pos_camera = f"{aspect['camera']['positive'] * 100:.2f}%"
    neu_camera = f"{aspect['camera']['neutral'] * 100:.2f}%"
    neg_camera = f"{aspect['camera']['negative'] * 100:.2f}%"

    pos_features = f"{aspect['features']['positive'] * 100:.2f}%"
    neu_features = f"{aspect['features']['neutral'] * 100:.2f}%"
    neg_features = f"{aspect['features']['negative'] * 100:.2f}%"

    pos_battery = f"{aspect['battery']['positive'] * 100:.2f}%"
    neu_battery = f"{aspect['battery']['neutral'] * 100:.2f}%"
    neg_battery = f"{aspect['battery']['negative'] * 100:.2f}%"

    pos_value = f"{aspect['value for money']['positive'] * 100:.2f}%"
    neu_value = f"{aspect['value for money']['neutral'] * 100:.2f}%"
    neg_value = f"{aspect['value for money']['negative'] * 100:.2f}%"

    ratings = df1['Ratings'].value_counts()
    numbers = ratings.index
    quantity = ratings.values
    labels = [f"Ratings {num}" for num in numbers]
    fig = px.pie(values=quantity, names=numbers, hole=0.5)
    div = fig.to_html(full_html=False)

    return render_template('Samsung S5.html', maxi=maxi, pos_score=pos_score, neg_score=neg_score,
                           neu_score=neu_score, pos_batterybackup=pos_batterybackup, 
                           neu_batterybackup=neu_batterybackup, 
                           neg_batterybackup=neg_batterybackup, 
                           pos_camera=pos_camera, 
                           neu_camera=neu_camera, 
                           neg_camera=neg_camera,
                           pos_features=pos_features, 
                           neu_features=neu_features, 
                           neg_features=neg_features,
                           pos_battery=pos_battery, 
                           neu_battery=neu_battery, 
                           neg_battery=neg_battery,
                           pos_value=pos_value, 
                           neu_value=neu_value, 
                           neg_value=neg_value,
                           plot_div=div)



@app.route('/samsungJ1')
def samsungJ1():
    df2 = pd.read_csv('samsung J1.csv')
    df_new2 = pd.read_csv('Samsung_J1_new.csv')
    maxi, dic = overview(df2)
    aspect = features(df_new2, df2)  
    pos_score = dic["Positive"]
    neg_score = dic["Negative"]
    neu_score = dic["Neutral"]
        # Convert the scores to percentages with 2 decimal places\\\\
    pos_batterybackup = f"{aspect['battery backup']['positive'] * 100:.2f}%"
    neu_batterybackup = f"{aspect['battery backup']['neutral'] * 100:.2f}%"
    neg_batterybackup = f"{aspect['battery backup']['negative'] * 100:.2f}%"

    pos_camera = f"{aspect['camera']['positive'] * 100:.2f}%"
    neu_camera = f"{aspect['camera']['neutral'] * 100:.2f}%"
    neg_camera = f"{aspect['camera']['negative'] * 100:.2f}%"

    pos_features = f"{aspect['features']['positive'] * 100:.2f}%"
    neu_features = f"{aspect['features']['neutral'] * 100:.2f}%"
    neg_features = f"{aspect['features']['negative'] * 100:.2f}%"

    pos_battery = f"{aspect['battery']['positive'] * 100:.2f}%"
    neu_battery = f"{aspect['battery']['neutral'] * 100:.2f}%"
    neg_battery = f"{aspect['battery']['negative'] * 100:.2f}%"

    pos_value = f"{aspect['value for money']['positive'] * 100:.2f}%"
    neu_value = f"{aspect['value for money']['neutral'] * 100:.2f}%"
    neg_value = f"{aspect['value for money']['negative'] * 100:.2f}%"

    ratings = df2['Ratings'].value_counts()
    numbers = ratings.index
    quantity = ratings.values
    labels = [f"Ratings {num}" for num in numbers]
    fig = px.pie(values=quantity, names=numbers, hole=0.5)
    div = fig.to_html(full_html=False)

    return render_template('SamsungGalaxyJ1Ace.html', maxi=maxi, pos_score=pos_score, neg_score=neg_score,
                           neu_score=neu_score, pos_batterybackup=pos_batterybackup, 
                           neu_batterybackup=neu_batterybackup, 
                           neg_batterybackup=neg_batterybackup, 
                           pos_camera=pos_camera, 
                           neu_camera=neu_camera, 
                           neg_camera=neg_camera,
                           pos_features=pos_features, 
                           neu_features=neu_features, 
                           neg_features=neg_features,
                           pos_battery=pos_battery, 
                           neu_battery=neu_battery, 
                           neg_battery=neg_battery,
                           pos_value=pos_value, 
                           neu_value=neu_value, 
                           neg_value=neg_value,
                           plot_div=div)


@app.route('/samsungA3')
def samsungA3():
    df3 = pd.read_csv('Samsung A3.csv')
    df_new3 = pd.read_csv('Samsung_A3_new.csv')
    maxi, dic = overview(df3)
    aspect = features(df_new3, df3)  
    pos_score = dic["Positive"]
    neg_score = dic["Negative"]
    neu_score = dic["Neutral"]
            # Convert the scores to percentages with 2 decimal places\\\\
    pos_batterybackup = f"{aspect['battery backup']['positive'] * 100:.2f}%"
    neu_batterybackup = f"{aspect['battery backup']['neutral'] * 100:.2f}%"
    neg_batterybackup = f"{aspect['battery backup']['negative'] * 100:.2f}%"

    pos_camera = f"{aspect['camera']['positive'] * 100:.2f}%"
    neu_camera = f"{aspect['camera']['neutral'] * 100:.2f}%"
    neg_camera = f"{aspect['camera']['negative'] * 100:.2f}%"

    pos_features = f"{aspect['features']['positive'] * 100:.2f}%"
    neu_features = f"{aspect['features']['neutral'] * 100:.2f}%"
    neg_features = f"{aspect['features']['negative'] * 100:.2f}%"

    pos_battery = f"{aspect['battery']['positive'] * 100:.2f}%"
    neu_battery = f"{aspect['battery']['neutral'] * 100:.2f}%"
    neg_battery = f"{aspect['battery']['negative'] * 100:.2f}%"

    pos_value = f"{aspect['value for money']['positive'] * 100:.2f}%"
    neu_value = f"{aspect['value for money']['neutral'] * 100:.2f}%"
    neg_value = f"{aspect['value for money']['negative'] * 100:.2f}%"

    ratings = df3['Ratings'].value_counts()
    numbers = ratings.index
    quantity = ratings.values
    labels = [f"Ratings {num}" for num in numbers]
    fig = px.pie(values=quantity, names=numbers, hole=0.5)
    div = fig.to_html(full_html=False)

    return render_template('samsung galaxy A3.html', maxi=maxi, pos_score=pos_score, neg_score=neg_score,
                           neu_score=neu_score, pos_batterybackup=pos_batterybackup, 
                           neu_batterybackup=neu_batterybackup, 
                           neg_batterybackup=neg_batterybackup, 
                           pos_camera=pos_camera, 
                           neu_camera=neu_camera, 
                           neg_camera=neg_camera,
                           pos_features=pos_features, 
                           neu_features=neu_features, 
                           neg_features=neg_features,
                           pos_battery=pos_battery, 
                           neu_battery=neu_battery, 
                           neg_battery=neg_battery,
                           pos_value=pos_value, 
                           neu_value=neu_value, 
                           neg_value=neg_value,
                           plot_div=div)

@app.route('/samsungA157')
def samsungA157():
    df4 = pd.read_csv('samsung a157.csv')
    df_new4 = pd.read_csv('Samsung_A157_new.csv')
    maxi, dic = overview(df4)
    aspect = features(df_new4, df4)  
    pos_score = dic["Positive"]
    neg_score = dic["Negative"]
    neu_score = dic["Neutral"]
    pos_batterybackup = f"{aspect['battery backup']['positive'] * 100:.2f}%"
    neu_batterybackup = f"{aspect['battery backup']['neutral'] * 100:.2f}%"
    neg_batterybackup = f"{aspect['battery backup']['negative'] * 100:.2f}%"

    pos_camera = f"{aspect['camera']['positive'] * 100:.2f}%"
    neu_camera = f"{aspect['camera']['neutral'] * 100:.2f}%"
    neg_camera = f"{aspect['camera']['negative'] * 100:.2f}%"

    pos_features = f"{aspect['features']['positive'] * 100:.2f}%"
    neu_features = f"{aspect['features']['neutral'] * 100:.2f}%"
    neg_features = f"{aspect['features']['negative'] * 100:.2f}%"

    pos_battery = f"{aspect['battery']['positive'] * 100:.2f}%"
    neu_battery = f"{aspect['battery']['neutral'] * 100:.2f}%"
    neg_battery = f"{aspect['battery']['negative'] * 100:.2f}%"

    pos_value = f"{aspect['value for money']['positive'] * 100:.2f}%"
    neu_value = f"{aspect['value for money']['neutral'] * 100:.2f}%"
    neg_value = f"{aspect['value for money']['negative'] * 100:.2f}%"

    ratings = df4['Ratings'].value_counts()
    numbers = ratings.index
    quantity = ratings.values
    labels = [f"Ratings {num}" for num in numbers]
    fig = px.pie(values=quantity, names=numbers, hole=0.5)
    div = fig.to_html(full_html=False)

    return render_template('samsung a157.HTML', maxi=maxi, pos_score=pos_score, neg_score=neg_score,
                           neu_score=neu_score, pos_batterybackup=pos_batterybackup, 
                           neu_batterybackup=neu_batterybackup, 
                           neg_batterybackup=neg_batterybackup, 
                           pos_camera=pos_camera, 
                           neu_camera=neu_camera, 
                           neg_camera=neg_camera,
                           pos_features=pos_features, 
                           neu_features=neu_features, 
                           neg_features=neg_features,
                           pos_battery=pos_battery, 
                           neu_battery=neu_battery, 
                           neg_battery=neg_battery,
                           pos_value=pos_value, 
                           neu_value=neu_value, 
                           neg_value=neg_value,
                           plot_div=div)



@app.route('/samsungA777')
def samsungA777():
    df5 = pd.read_csv('samsung a777.csv')
    df_new5 = pd.read_csv('Samsung_A777_new.csv')
    maxi, dic = overview(df5)
    aspect = features(df_new5, df5)  
    pos_score = dic["Positive"]
    neg_score = dic["Negative"]
    neu_score = dic["Neutral"]
    pos_batterybackup = f"{aspect['battery backup']['positive'] * 100:.2f}%"
    neu_batterybackup = f"{aspect['battery backup']['neutral'] * 100:.2f}%"
    neg_batterybackup = f"{aspect['battery backup']['negative'] * 100:.2f}%"

    pos_camera = f"{aspect['camera']['positive'] * 100:.2f}%"
    neu_camera = f"{aspect['camera']['neutral'] * 100:.2f}%"
    neg_camera = f"{aspect['camera']['negative'] * 100:.2f}%"

    pos_features = f"{aspect['features']['positive'] * 100:.2f}%"
    neu_features = f"{aspect['features']['neutral'] * 100:.2f}%"
    neg_features = f"{aspect['features']['negative'] * 100:.2f}%"

    pos_battery = f"{aspect['battery']['positive'] * 100:.2f}%"
    neu_battery = f"{aspect['battery']['neutral'] * 100:.2f}%"
    neg_battery = f"{aspect['battery']['negative'] * 100:.2f}%"

    pos_value = f"{aspect['value for money']['positive'] * 100:.2f}%"
    neu_value = f"{aspect['value for money']['neutral'] * 100:.2f}%"
    neg_value = f"{aspect['value for money']['negative'] * 100:.2f}%"

    ratings = df5['Ratings'].value_counts()
    numbers = ratings.index
    quantity = ratings.values
    labels = [f"Ratings {num}" for num in numbers]
    fig = px.pie(values=quantity, names=numbers, hole=0.5)
    div = fig.to_html(full_html=False)

    return render_template('Samsung SGH.html', maxi=maxi, pos_score=pos_score, neg_score=neg_score,
                           neu_score=neu_score, pos_batterybackup=pos_batterybackup, 
                           neu_batterybackup=neu_batterybackup, 
                           neg_batterybackup=neg_batterybackup, 
                           pos_camera=pos_camera, 
                           neu_camera=neu_camera, 
                           neg_camera=neg_camera,
                           pos_features=pos_features, 
                           neu_features=neu_features, 
                           neg_features=neg_features,
                           pos_battery=pos_battery, 
                           neu_battery=neu_battery, 
                           neg_battery=neg_battery,
                           pos_value=pos_value, 
                           neu_value=neu_value, 
                           neg_value=neg_value,
                           plot_div=div)


@app.route('/SamsungNote4')
def SamsungNote4():
    df6 = pd.read_csv('Samsung_galaxy_note4.csv')
    df_new6 = pd.read_csv('Samsung_note4_new.csv')
    maxi, dic = overview(df6)
    aspect = features(df_new6, df6)  
    pos_score = dic["Positive"]
    neg_score = dic["Negative"]
    neu_score = dic["Neutral"]
    pos_batterybackup = f"{aspect['battery backup']['positive'] * 100:.2f}%"
    neu_batterybackup = f"{aspect['battery backup']['neutral'] * 100:.2f}%"
    neg_batterybackup = f"{aspect['battery backup']['negative'] * 100:.2f}%"

    pos_camera = f"{aspect['camera']['positive'] * 100:.2f}%"
    neu_camera = f"{aspect['camera']['neutral'] * 100:.2f}%"
    neg_camera = f"{aspect['camera']['negative'] * 100:.2f}%"

    pos_features = f"{aspect['features']['positive'] * 100:.2f}%"
    neu_features = f"{aspect['features']['neutral'] * 100:.2f}%"
    neg_features = f"{aspect['features']['negative'] * 100:.2f}%"

    pos_battery = f"{aspect['battery']['positive'] * 100:.2f}%"
    neu_battery = f"{aspect['battery']['neutral'] * 100:.2f}%"
    neg_battery = f"{aspect['battery']['negative'] * 100:.2f}%"

    pos_value = f"{aspect['value for money']['positive'] * 100:.2f}%"
    neu_value = f"{aspect['value for money']['neutral'] * 100:.2f}%"
    neg_value = f"{aspect['value for money']['negative'] * 100:.2f}%"

    ratings = df6['Ratings'].value_counts()
    numbers = ratings.index
    quantity = ratings.values
    labels = [f"Ratings {num}" for num in numbers]
    fig = px.pie(values=quantity, names=numbers, hole=0.5)
    div = fig.to_html(full_html=False)

    return render_template('SamsungGalaxyNote4.html', maxi=maxi, pos_score=pos_score, neg_score=neg_score,
                           neu_score=neu_score, pos_batterybackup=pos_batterybackup, 
                           neu_batterybackup=neu_batterybackup, 
                           neg_batterybackup=neg_batterybackup, 
                           pos_camera=pos_camera, 
                           neu_camera=neu_camera, 
                           neg_camera=neg_camera,
                           pos_features=pos_features, 
                           neu_features=neu_features, 
                           neg_features=neg_features,
                           pos_battery=pos_battery, 
                           neu_battery=neu_battery, 
                           neg_battery=neg_battery,
                           pos_value=pos_value, 
                           neu_value=neu_value, 
                           neg_value=neg_value,
                           plot_div=div)


@app.route('/SamsungNote5')
def SamsungNote5():
    df7 = pd.read_csv('Samsunggalaxy_Note5.csv')
    df_new7 = pd.read_csv('Samsunggalaxy_note5_new.csv')
    maxi, dic = overview(df7)
    aspect = features(df_new7, df7)  
    pos_score = dic["Positive"]
    neg_score = dic["Negative"]
    neu_score = dic["Neutral"]
    pos_batterybackup = f"{aspect['battery backup']['positive'] * 100:.2f}%"
    neu_batterybackup = f"{aspect['battery backup']['neutral'] * 100:.2f}%"
    neg_batterybackup = f"{aspect['battery backup']['negative'] * 100:.2f}%"

    pos_camera = f"{aspect['camera']['positive'] * 100:.2f}%"
    neu_camera = f"{aspect['camera']['neutral'] * 100:.2f}%"
    neg_camera = f"{aspect['camera']['negative'] * 100:.2f}%"

    pos_features = f"{aspect['features']['positive'] * 100:.2f}%"
    neu_features = f"{aspect['features']['neutral'] * 100:.2f}%"
    neg_features = f"{aspect['features']['negative'] * 100:.2f}%"

    pos_battery = f"{aspect['battery']['positive'] * 100:.2f}%"
    neu_battery = f"{aspect['battery']['neutral'] * 100:.2f}%"
    neg_battery = f"{aspect['battery']['negative'] * 100:.2f}%"

    pos_value = f"{aspect['value for money']['positive'] * 100:.2f}%"
    neu_value = f"{aspect['value for money']['neutral'] * 100:.2f}%"
    neg_value = f"{aspect['value for money']['negative'] * 100:.2f}%"

    ratings = df7['Ratings'].value_counts()
    numbers = ratings.index
    quantity = ratings.values
    labels = [f"Ratings {num}" for num in numbers]
    fig = px.pie(values=quantity, names=numbers, hole=0.5)
    div = fig.to_html(full_html=False)

    return render_template('SamsungGalaxy Note5.html', maxi=maxi, pos_score=pos_score, neg_score=neg_score,
                           neu_score=neu_score, pos_batterybackup=pos_batterybackup, 
                           neu_batterybackup=neu_batterybackup, 
                           neg_batterybackup=neg_batterybackup, 
                           pos_camera=pos_camera, 
                           neu_camera=neu_camera, 
                           neg_camera=neg_camera,
                           pos_features=pos_features, 
                           neu_features=neu_features, 
                           neg_features=neg_features,
                           pos_battery=pos_battery, 
                           neu_battery=neu_battery, 
                           neg_battery=neg_battery,
                           pos_value=pos_value, 
                           neu_value=neu_value, 
                           neg_value=neg_value,
                           plot_div=div)



@app.route('/Samsung805f')
def Samsung805f():
    df8 = pd.read_csv('samsung galaxy g805f.csv')
    df_new8 = pd.read_csv('Samsung_galaxy_g805_new.csv')
    maxi, dic = overview(df8)
    aspect = features(df_new8, df8)  
    pos_score = dic["Positive"]
    neg_score = dic["Negative"]
    neu_score = dic["Neutral"]
    pos_batterybackup = f"{aspect['battery backup']['positive'] * 100:.2f}%"
    neu_batterybackup = f"{aspect['battery backup']['neutral'] * 100:.2f}%"
    neg_batterybackup = f"{aspect['battery backup']['negative'] * 100:.2f}%"

    pos_camera = f"{aspect['camera']['positive'] * 100:.2f}%"
    neu_camera = f"{aspect['camera']['neutral'] * 100:.2f}%"
    neg_camera = f"{aspect['camera']['negative'] * 100:.2f}%"

    pos_features = f"{aspect['features']['positive'] * 100:.2f}%"
    neu_features = f"{aspect['features']['neutral'] * 100:.2f}%"
    neg_features = f"{aspect['features']['negative'] * 100:.2f}%"

    pos_battery = f"{aspect['battery']['positive'] * 100:.2f}%"
    neu_battery = f"{aspect['battery']['neutral'] * 100:.2f}%"
    neg_battery = f"{aspect['battery']['negative'] * 100:.2f}%"

    pos_value = f"{aspect['value for money']['positive'] * 100:.2f}%"
    neu_value = f"{aspect['value for money']['neutral'] * 100:.2f}%"
    neg_value = f"{aspect['value for money']['negative'] * 100:.2f}%"

    ratings = df8['Ratings'].value_counts()
    numbers = ratings.index
    quantity = ratings.values
    labels = [f"Ratings {num}" for num in numbers]
    fig = px.pie(values=quantity, names=numbers, hole=0.5)
    div = fig.to_html(full_html=False)

    return render_template('Samsung Galaxy Alpha.html', maxi=maxi, pos_score=pos_score, neg_score=neg_score,
                           neu_score=neu_score, pos_batterybackup=pos_batterybackup, 
                           neu_batterybackup=neu_batterybackup, 
                           neg_batterybackup=neg_batterybackup, 
                           pos_camera=pos_camera, 
                           neu_camera=neu_camera, 
                           neg_camera=neg_camera,
                           pos_features=pos_features, 
                           neu_features=neu_features, 
                           neg_features=neg_features,
                           pos_battery=pos_battery, 
                           neu_battery=neu_battery, 
                           neg_battery=neg_battery,
                           pos_value=pos_value, 
                           neu_value=neu_value, 
                           neg_value=neg_value,
                           plot_div=div)



@app.route('/SamsungJ5')
def SamsungJ5():
    df9 = pd.read_csv('samsung galaxy J5.csv')
    df_new9 = pd.read_csv('Samsunggalaxy_J5_new.csv')
    maxi, dic = overview(df9)
    aspect = features(df_new9, df9)  
    pos_score = dic["Positive"]
    neg_score = dic["Negative"]
    neu_score = dic["Neutral"]
    pos_batterybackup = f"{aspect['battery backup']['positive'] * 100:.2f}%"
    neu_batterybackup = f"{aspect['battery backup']['neutral'] * 100:.2f}%"
    neg_batterybackup = f"{aspect['battery backup']['negative'] * 100:.2f}%"

    pos_camera = f"{aspect['camera']['positive'] * 100:.2f}%"
    neu_camera = f"{aspect['camera']['neutral'] * 100:.2f}%"
    neg_camera = f"{aspect['camera']['negative'] * 100:.2f}%"

    pos_features = f"{aspect['features']['positive'] * 100:.2f}%"
    neu_features = f"{aspect['features']['neutral'] * 100:.2f}%"
    neg_features = f"{aspect['features']['negative'] * 100:.2f}%"

    pos_battery = f"{aspect['battery']['positive'] * 100:.2f}%"
    neu_battery = f"{aspect['battery']['neutral'] * 100:.2f}%"
    neg_battery = f"{aspect['battery']['negative'] * 100:.2f}%"

    pos_value = f"{aspect['value for money']['positive'] * 100:.2f}%"
    neu_value = f"{aspect['value for money']['neutral'] * 100:.2f}%"
    neg_value = f"{aspect['value for money']['negative'] * 100:.2f}%"

    ratings = df9['Ratings'].value_counts()
    numbers = ratings.index
    quantity = ratings.values
    labels = [f"Ratings {num}" for num in numbers]
    fig = px.pie(values=quantity, names=numbers, hole=0.5)
    div = fig.to_html(full_html=False)

    return render_template('SamsungGalaxyJ5.html', maxi=maxi, pos_score=pos_score, neg_score=neg_score,
                           neu_score=neu_score, pos_batterybackup=pos_batterybackup, 
                           neu_batterybackup=neu_batterybackup, 
                           neg_batterybackup=neg_batterybackup, 
                           pos_camera=pos_camera, 
                           neu_camera=neu_camera, 
                           neg_camera=neg_camera,
                           pos_features=pos_features, 
                           neu_features=neu_features, 
                           neg_features=neg_features,
                           pos_battery=pos_battery, 
                           neu_battery=neu_battery, 
                           neg_battery=neg_battery,
                           pos_value=pos_value, 
                           neu_value=neu_value, 
                           neg_value=neg_value,
                           plot_div=div)


@app.route('/samsungA323')
def samsungA323():
    df10 = pd.read_csv('Samsung Note 3 - Samsung Note 3.csv')
    df_new10 = pd.read_csv('Samsung_note3_new.csv')
    maxi, dic = overview(df10)
    aspect = features(df_new10, df10)  
    pos_score = dic["Positive"]
    neg_score = dic["Negative"]
    neu_score = dic["Neutral"]
    pos_batterybackup = f"{aspect['battery backup']['positive'] * 100:.2f}%"
    neu_batterybackup = f"{aspect['battery backup']['neutral'] * 100:.2f}%"
    neg_batterybackup = f"{aspect['battery backup']['negative'] * 100:.2f}%"

    pos_camera = f"{aspect['camera']['positive'] * 100:.2f}%"
    neu_camera = f"{aspect['camera']['neutral'] * 100:.2f}%"
    neg_camera = f"{aspect['camera']['negative'] * 100:.2f}%"

    pos_features = f"{aspect['features']['positive'] * 100:.2f}%"
    neu_features = f"{aspect['features']['neutral'] * 100:.2f}%"
    neg_features = f"{aspect['features']['negative'] * 100:.2f}%"

    pos_battery = f"{aspect['battery']['positive'] * 100:.2f}%"
    neu_battery = f"{aspect['battery']['neutral'] * 100:.2f}%"
    neg_battery = f"{aspect['battery']['negative'] * 100:.2f}%"

    pos_value = f"{aspect['value for money']['positive'] * 100:.2f}%"
    neu_value = f"{aspect['value for money']['neutral'] * 100:.2f}%"
    neg_value = f"{aspect['value for money']['negative'] * 100:.2f}%"

    ratings = df10['Ratings'].value_counts()
    numbers = ratings.index
    quantity = ratings.values
    labels = [f"Ratings {num}" for num in numbers]
    fig = px.pie(values=quantity, names=numbers, hole=0.5)
    div = fig.to_html(full_html=False)

    return render_template('SamsungGalaxyNote 3.html', maxi=maxi, pos_score=pos_score, neg_score=neg_score,
                           neu_score=neu_score, pos_batterybackup=pos_batterybackup, 
                           neu_batterybackup=neu_batterybackup, 
                           neg_batterybackup=neg_batterybackup, 
                           pos_camera=pos_camera, 
                           neu_camera=neu_camera, 
                           neg_camera=neg_camera,
                           pos_features=pos_features, 
                           neu_features=neu_features, 
                           neg_features=neg_features,
                           pos_battery=pos_battery, 
                           neu_battery=neu_battery, 
                           neg_battery=neg_battery,
                           pos_value=pos_value, 
                           neu_value=neu_value, 
                           neg_value=neg_value,
                           plot_div=div)


if __name__ == '__main__':
    app.run(debug=True)