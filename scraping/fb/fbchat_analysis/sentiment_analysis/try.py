import operator
from compare_friends import *

# collapse pos and neg sentiments into a single metric ranging from -1 to 1
colp = {}
for friend, l in to_sentiments.items():
    count = 0
    for sentiment in l:
        if sentiment == 'neg':
            count -= 1
        if sentiment == 'pos':
            count += 1
    colp[friend] = count / len(l)

# adjust metrics so that median is at 0
srtd = sorted(colp.items(), key=operator.itemgetter(1))
median = srtd[int(len(srtd) / 2)]

for friend, value in colp.items():
    colp[friend] -= median[1]

summs = 0
count = 0

for friend in colp.keys():
    summs += colp[friend]
    count += 1

average = summs/count

f = open("messenger_emotion_score", "w")
f.write(str(average))
f.close()
