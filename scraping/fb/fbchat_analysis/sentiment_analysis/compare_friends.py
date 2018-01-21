import fbchat
import FBBack
import os
from pull_messages import *
from classify import Classifier
from base import *

client = fbchat.Client(os.environ['ID'], os.environ['PASSWORD'])

while True:
    file_mode = input('r: read/ w+: read n write ')
    save_path = '/Users/mananaggarwal/Downloads/fbchat_analysis-master/fbchat_analysis/sentiment_analysis/'
    complete_name = os.path.join(save_path, 'friends_short.txt')

    if file_mode == 'r':
        friends_file = open(complete_name, 'r')
        print('opening...\n')
        break
    elif file_mode == 'w+':
        friends_file = open(complete_name, 'w+')
        print("enter the names of your FB contacts [Ctrl-D to save it]: ")
        while True:
            try:
                line = input()
            except EOFError:
                break
            friends_file.write('%r\n' %line)
        break
    else:
        print('incorrect input, please try again\n')

friends_file.seek(0)
c = Classifier()

from_lengths = {}
to_lengths = {}
from_sentiments = {}
to_sentiments = {}

friends = []

for l in friends_file:
    a,b = l.split(" ")
    friend_name = a + ' ' + b
    friends.append(friend_name)

for friend_name in friends:
    print(friend_name)

    print('pulling messages')
    (you_messages, friend_messages) = pull_messages(client, friend_name)
    from_lengths[friend_name] = len(friend_messages)
    to_lengths[friend_name] = len(you_messages)

    print('classifying')
    (you_sentiments, friend_sentiments) = c.classify_from_lists(you_messages, friend_messages)
    from_sentiments[friend_name] = friend_sentiments
    to_sentiments[friend_name] = you_sentiments

    print()
    friends_file.close()
