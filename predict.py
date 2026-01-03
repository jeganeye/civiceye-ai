import joblib

# Load model and vectorizer
model = joblib.load("issue_classifier.pkl")
vectorizer = joblib.load("vectorizer.pkl")

print("Enter issues separated by semicolon (;)")
user_input = input("Issues: ")

# Split multiple issues
issues = [issue.strip() for issue in user_input.split(";") if issue.strip()]

if not issues:
    print("No issues entered.")
else:
    X = vectorizer.transform(issues)
    predictions = model.predict(X)

    print("\nPrediction Results:")
    for i, (issue, category) in enumerate(zip(issues, predictions), start=1):
        print(f"{i}. {issue} → {category}")
