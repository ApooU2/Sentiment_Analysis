from textblob import TextBlob

def analyze_sentiment(texts):
	sentiment_scores = []
	for text in texts:
		analysis = TextBlob(text)
		sentiment_scores.append(analysis.sentiment.polarity)
	if sentiment_scores:
		avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
		return avg_sentiment
	return 0