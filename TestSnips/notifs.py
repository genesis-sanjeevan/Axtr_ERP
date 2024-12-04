import pandas as pd
import numpy as np
import pprint
import datetime

ls = pd.read_csv("Z:\PSG\FYear Project\Project\Flask Web App\Website\Dataset\Log Sheets\RF-2907_MOHAMED_RAUF_ALI_S.csv", usecols=['DATE','MAN_HOURS'])

dates=ls['DATE'].tolist()
man_hours=ls['MAN_HOURS'].tolist()

x=zip(dates,man_hours)
l=list(x)
d=dict()

for i in l:
    if i[0] is not np.nan:
        d[i[0]]=0

for j in l:
    if j[1] is not np.nan and j[0] is not np.nan:
        d[j[0]]+=j[1]

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
date_string = f"{year}-{month:02d}-{day:02d}"

for key, value in d.items():
  if key == date_string:
    b = {value}
    for i in b:
        if i < 8:
            print("yess ",8-i," wooho")
            print("Today's log entered successfully ({a})({hours} hours)".format(a=date_string, hours=i))
        elif i == 8:
            print("yess")
        else:
            print("noo")
    # if int(b) < 8:
    #     print("ohh yeahh babyy!!")
    # elif int(b) == 8:
    #     print("Congratulations")
    # else:
    #     print("YOu are promoted!")

