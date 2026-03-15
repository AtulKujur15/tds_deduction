import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix
import joblib

tds_dataset=pd.read_csv("data/tds_large_dataset_india.csv")
payment=LabelEncoder()
vendor=LabelEncoder()
pan=LabelEncoder()

tds_dataset["Payment_Type"]=payment.fit_transform(tds_dataset["Payment_Type"])
tds_dataset["Vendor_Type"]=vendor.fit_transform(tds_dataset["Vendor_Type"])
tds_dataset["PAN_Available"]=pan.fit_transform(tds_dataset["PAN_Available"])

print(tds_dataset)

X=tds_dataset[["Payment_Type","Amount","Vendor_Type","PAN_Available"]]
y=tds_dataset["TDS_Rate"]

X_train,X_test,y_train,y_test=train_test_split(
X,y,test_size=0.2,random_state=42)

model=RandomForestClassifier()
model.fit(X_train,y_train)
y_pred=model.predict(X_test)

accuracy=   accuracy_score(y_test,y_pred)
print("Model Accuracy:",accuracy)

CM=   confusion_matrix(y_test,y_pred)
print(CM)


joblib.dump(model,"tds_model.pkl")
print("Model Trained Succesfully")
