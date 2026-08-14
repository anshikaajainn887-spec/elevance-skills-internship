from textblob import TextBlob

def analyze_sentiment(message):
    analysis = TextBlob(message)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        sentiment = "POSITIVE"
        response = "😊 I'm glad you're feeling positive! How can I help you further?"
    elif polarity < 0:
        sentiment = "NEGATIVE"
        response = "😔 I'm sorry you're having a difficult experience. I'll do my best to help."
    else:
        sentiment = "NEUTRAL"
        response = "😐 Thanks for sharing. How can I assist you?"

    return {
        "sentiment": sentiment,
        "confidence": round(abs(polarity), 2),
        "response": response
    }