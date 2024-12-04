import tqdm
import time
import pprint
import datetime

dates=[]

for i in tqdm.trange(2023,2054):
    for j in range(1,13):
        l=[]
        sat=[]
        time.sleep(0.05)
        for k in range(1,32):
            try:
                date=datetime.datetime(i,j,k)
                if date.weekday()==5:
                    sat.append(date)
                elif date.weekday() ==6:
                    l.append(date)
                else:
                    pass
            except:
                pass
        l.append(sat[1])
        l.append(sat[3])
        l.sort()
        for x in l:
            dates.append(x.strftime("%Y-%m-%d"))
        
print(dates)
