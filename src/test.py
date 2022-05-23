from datetime import datetime as dt
n = str(dt.now())
#with open("../data/treddit_"+n[:4]+n[5:7]+n[8:10]+"_"+n[11:13]+n[14:16]+n[17:19]+".csv", "+w") as f:
for i in range(5):
    with open("../data/tett_" + ".csv", "+w") as f:
        f.write("test" + str(i))

