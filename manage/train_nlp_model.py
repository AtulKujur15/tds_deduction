import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

data=pd.read_csv("data\payment_text_dataset.csv")
print(data)



X=data["description"]
y=data["category"]

model=Pipeline([
    ("tfidf",TfidfVectorizer()),
    ("clf",MultinomialNB())
])

model.fit(X,y)

joblib.dump(model,"model/payment_text_model.pkl")

print("NLP model train succesfully")
