import os 
import pandas as pd
from pandas import ExcelWriter
import matplotlib.pyplot as plt
import re

pd.set_option('display.max_columns',4)
pd.set_option('display.max_rows', 10)
path="C:\\Users\\yesta\\Desktop"
os.chdir(path)

df = pd.read_excel("budget copy.xlsx", "Sheet2")

date_pattern = r'([0-9]{4}-[0-9]{2}-[0-9]{2})'
row1 = df.iloc[:,0]
#print(row1)

all_dates = {}

first_date = str(df.columns.values[0])[:10]
all_dates[0] = first_date

i = 0
j = 1
for i in range(0, len(row1)):
    date = re.search(date_pattern, str(row1[i]))
    if date:
       # print(date.group())
        all_dates[j] = date.group()
        j += 1

for thing in all_dates:
    print(thing, all_dates[thing])

cycle_dates = {int(k/2):v for (k,v) in all_dates.items() if k%2==0}
print(cycle_dates)

offset = 3
total_cols = (len(df.columns)+1)
df.drop(df.iloc[:, 1:total_cols:offset], axis=1, inplace=True)

cycle = 48
no_cycles = int(df.index[-1] / cycle)

def clean_df(df):
    df = df.dropna(how="all")

    df2 = df.iloc[:,0:total_cols:2]
  
    df2 = df2.melt().drop('variable',axis=1).rename({"value": "expense"}, axis=1)
    df2 = df2.dropna(how="all")

    df4 = df.iloc[:,1:total_cols:2]
    df5 = df4.melt().drop('variable',axis=1).rename({"value": "amount"}, axis=1)
    df5 = df5.dropna(how="all")

    df2["amount"] = df5.abs()
    df2.columns = ["expense", "amount"]

    df2 = df2.groupby("expense", as_index=False).sum()

    i = df2[(df2["expense"] == "Income")]
    df2 = df2.drop(i.index, axis=0)

    df2 = df2.sort_values(by=["amount"], ascending = False)

    return df2

def make_graph(df):
    plot = df.plot.pie(y="amount", labels=df["expense"], autopct='%1.0f%%')
   # plt.show()

df_dict = {}
i = 0
writer = pd.ExcelWriter("budget copy.xlsx", engine = 'openpyxl', mode='a', if_sheet_exists='overlay')
while (i < (no_cycles)):
    df1 = df.iloc[0:48, :]
    df1 = df1.drop([20, 24, 45, 46], axis=0)
    df1 = clean_df(df1)
    df_dict[i] = df1

    df1.to_excel(writer, sheet_name = cycle_dates[i], index=False)
    make_graph(df1)

    df = df.tail(-50)
    df.reset_index(drop=True, inplace=True)
    
    i = i + 1
writer.close()
