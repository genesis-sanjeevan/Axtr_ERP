import pandas as pd
import numpy as np
import pprint

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

pprint.pprint(d)
