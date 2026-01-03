import pandas as pd              # for handling data
import re                        # for text cleaning
import nltk                      # for NLP support
from textblob import TextBlob    # for sentiment analysis
import matplotlib.pyplot as plt  # for visualization

nltk.download('punkt')

# Sample public text data
data = {
    "Source": [
        "Amazon", "Amazon", "Twitter", "Twitter", "News", "News",
        "Amazon", "Twitter", "News", "Amazon", "Twitter", "News"
    ],
    "Text": [
        "I absolutely love this phone, amazing performance!",
        "Very bad quality, totally disappointed.",
        "This update made me so happy!",
        "Worst service ever, I hate it.",
        "The government policy was well received by the public.",
        "Citizens are angry about rising prices.",
        "Product is okay, nothing special.",
        "Feeling sad about today’s incident.",
        "The economy shows positive growth signs.",
        "Terrible packaging but good product.",
        "I am excited for the new movie release!",
        "People are worried about climate change."
    ]
}

df = pd.DataFrame(data)   # create table

def clean_text(text):
    text = text.lower()                 # lowercase text
    text = re.sub(r'[^a-z\s]', '', text) # remove symbols
    return text

df['Clean_Text'] = df['Text'].apply(clean_text)

def sentiment_score(text):
    return TextBlob(text).sentiment.polarity  # emotion strength

def sentiment_label(score):
    if score > 0.1:
        return "Positive"
    elif score < -0.1:
        return "Negative"
    else:
        return "Neutral"

def emotion_detection(text):
    joy = ["love", "happy", "excited", "amazing", "good", "positive"]
    anger = ["hate", "worst", "angry", "bad", "terrible"]
    sadness = ["sad", "worried", "disappointed"]
    
    if any(word in text for word in joy):
        return "Joy"
    elif any(word in text for word in anger):
        return "Anger"
    elif any(word in text for word in sadness):
        return "Sadness"
    else:
        return "Neutral"

df['Sentiment_Score'] = df['Clean_Text'].apply(sentiment_score)
df['Sentiment'] = df['Sentiment_Score'].apply(sentiment_label)
df['Emotion'] = df['Clean_Text'].apply(emotion_detection)
df['Word_Count'] = df['Text'].apply(lambda x: len(x.split()))

for i, row in df.iterrows():
    print("\nText", i+1)
    print("Source    :", row['Source'])
    print("Text      :", row['Text'])
    print("Sentiment :", row['Sentiment'])
    print("Emotion   :", row['Emotion'])
    print("Score     :", round(row['Sentiment_Score'], 2))
    print("Words     :", row['Word_Count'])
    print("-" * 50)

sentiment_counts = df['Sentiment'].value_counts()
emotion_counts = df['Emotion'].value_counts()

plt.figure()
sentiment_counts.plot(kind='bar')
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.show()

plt.figure()
emotion_counts.plot(kind='bar')
plt.title("Emotion Distribution")
plt.xlabel("Emotion")
plt.ylabel("Frequency")
plt.show()

plt.figure()
emotion_counts.plot(kind='pie', autopct='%1.1f%%')
plt.title("Emotion Share")
plt.ylabel("")
plt.show()

average_sentiment = df.groupby('Source')['Sentiment_Score'].mean()
print("\nAverage Sentiment by Source")
print(average_sentiment)

negative_percentage = (df[df['Sentiment'] == 'Negative'].shape[0] / len(df)) * 100
print("\nNegative Opinion Percentage:", round(negative_percentage, 2), "%")

df.to_csv("public_opinion_sentiment_analysis.csv", index=False)

print("\nSentiment Analysis Completed")
