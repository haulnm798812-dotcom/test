import pandas as pd
import csv
df = pd.read_csv("habittracker.txt", index_col=False)
df.to_csv("habittracker.csv", index=False)
