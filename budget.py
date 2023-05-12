import os 
import pandas as pd
from pandas import ExcelWriter
import matplotlib.pyplot as plt

pd.set_option('display.max_columns',4)
pd.set_option('display.max_rows', None)
path="C:\\Users\\yesta\\Desktop"
os.chdir(path)

df = pd.read_excel("budtest.xlsx", "Sheet2")

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
    plt.show()

df_dict = {}
i = 1
writer = pd.ExcelWriter("budtest.xlsx", engine = 'openpyxl', mode='a', if_sheet_exists='overlay')
while (i < (no_cycles)+1):
    df1 = df.iloc[0:48, :]
    df1 = df1.drop([20, 24, 45, 46], axis=0)
    df1 = clean_df(df1)
    df_dict[i] = df1

    df1.to_excel(writer, sheet_name = 'cycle' + str(i), index=False)
    make_graph(df1)

    df = df.tail(-50)
    df.reset_index(drop=True, inplace=True)
    
    i = i + 1
writer.close()