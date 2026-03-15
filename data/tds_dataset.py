import pandas as pd
tds_dataset=pd.read_csv("data/tds_large_dataset_india.csv")
print(tds_dataset.info())
# print(tds_dataset.describe())
print(tds_dataset.head())