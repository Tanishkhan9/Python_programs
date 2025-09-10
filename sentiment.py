import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure NLTK data is downloaded (only needs to run once)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('vader_lexicon', quiet=True)

def analyze_statements(statements):
    stop_words = set(stopwords.words('english'))
    sia = SentimentIntensityAnalyzer()
    all_words = []
    analysis_results = []

    for idx, stmt in enumerate(statements, 1):
        words = word_tokenize(stmt)
        words_clean = [w.lower() for w in words if w.isalpha() and w.lower() not in stop_words]
        all_words.extend(words_clean)
        sentiment = sia.polarity_scores(stmt)
        sentiment_label = (
            "Positive" if sentiment['compound'] > 0.2 else
            "Negative" if sentiment['compound'] < -0.2 else
            "Neutral"
        )
        analysis_results.append({
            "Statement #": idx,
            "Text": stmt,
            "Word Count": len(words_clean),
            "Sentiment": sentiment_label,
            "Sentiment Scores": sentiment
        })

    # Global analysis
    most_common = Counter(all_words).most_common(10)
    print("\n--- Statement Analysis ---")
    for result in analysis_results:
        print(f"\nStatement #{result['Statement #']}: {result['Text']}")
        print(f"  Word Count: {result['Word Count']}")
        print(f"  Sentiment: {result['Sentiment']} (Scores: {result['Sentiment Scores']})")

    print("\n--- Overall Analysis ---")
    print(f"Total Statements: {len(statements)}")
    print(f"Total Words (excluding stopwords): {len(all_words)}")
    print("Most Common Words:")
    for word, count in most_common:
        print(f"  {word}: {count}")

if __name__ == "__main__":
    print("Enter your statements (one per line, blank line to finish):")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line.strip())
    if lines:
        analyze_statements(lines)
    else:
        print("No statements entered.")
