# train_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Step 1: Load dataset
data = pd.read_csv('dataset.csv')

# Step 2: Split features and labels
X = data['text']
y = data['label']

# Step 3: Convert text to numerical features
vectorizer = TfidfVectorizer()
X_vect = vectorizer.fit_transform(X)

# Step 4: Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.2, random_state=42)

# Step 5: Train classifier
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 6: Evaluate model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Step 7: Save the model and vectorizer
joblib.dump(model, 'issue_classifier.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
print("Model and vectorizer saved successfully!")

# --- Step 8: Predict new issues ---
# Example text to classify
new_issues = [
    "The street light is broken near my house",
    "Garbage not collected for two days",
    "Water supply is leaking from pipe"
]

# Transform and predict
X_new = vectorizer.transform(new_issues)
predictions = model.predict(X_new)

# Print results
for issue, category in zip(new_issues, predictions):
    print(f"Issue: {issue}\nPredicted category: {category}\n")
