import os 
import pandas as pd
import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.use('TkAgg') 

pd.set_option('display.max_columns',4)
pd.set_option('display.max_rows', None)

path="C:\\Users\\yesta\\Desktop"
os.chdir(path)

df = pd.read_excel("budget copy.xlsx", "Sheet2")
#print(df)

offset = 3
total_cols = (len(df.columns)+1)
df.drop(df.iloc[:, 1:total_cols:offset], axis=1, inplace=True)

#print(df)

cycle = 48
no_cycles = int(df.index[-1] / cycle)
#print(no_cycles)

#print(df)
#20 24 45 46 50 71 75 

# df = df.iloc[0:47, :]
# df = df.dropna(how="all")
# df.drop([20, 24, 45, 46], axis=0, inplace=True)
#print(df)

df_dict = {}
i = 1
while (i < (no_cycles)+1):
    df1 = df.iloc[0:48, :]
   # print(df)
  #  df = df.dropna(how="all")
    #print(df1)
    df1 = df1.drop([20, 24, 45, 46], axis=0)
    df_dict[i] = df1
    df = df.tail(-50)
    df.reset_index(drop=True, inplace=True)
   # print(df)
   # print("done")
    i = i + 1




#df.drop(df.columns[[1, 4, 7, 10, 13, 16, 19, 21, 22, 23]], axis=1, inplace=True)
#df.drop([20, 24, 45, 46], axis=0, inplace=True)

def clean_df(df):
    df = df.dropna(how="all")
    # print(df)
    # print(df.head())

    df2 = df.iloc[:,0:total_cols:2]
    #print(df2)
    #print(df2.head())
    df2 = df2.melt().drop('variable',axis=1).rename({"value": "expense"}, axis=1)
    df2 = df2.dropna(how="all")
    #print(df2)

    df4 = df.iloc[:,1:total_cols:2]
    df5 = df4.melt().drop('variable',axis=1).rename({"value": "amount"}, axis=1)
    df5 = df5.dropna(how="all")
    #print(df5)

    df2["amount"] = df5.abs()
    df2.columns = ["expense", "amount"]

    df2 = df2.groupby("expense", as_index=False).sum()
    #print(df2)

    i = df2[(df2["expense"] == "Income")]
    df2 = df2.drop(i.index, axis=0)

    df2 = df2.sort_values(by=["amount"], ascending = False)

    return df2

def make_graph(df):
    plot = df.plot.pie(y="amount", labels=df["expense"], autopct='%1.1f%%')
   # plt.show()

i = 1
while i < (no_cycles+1):
    a = (clean_df(df_dict[i]))
    print("cycle", i, "\n", a, "\n")
    make_graph(a)
    i += 1


#df.to_excel("output.xlsx") 