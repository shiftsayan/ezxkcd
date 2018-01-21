import fbchat
import FBBack
import os
from base import *

def pull_messages(client, friend_name):
    friendList = client.searchForUsers(friend_name)
    if len(friendList) == 0:
        return []
    else:
        friend = friendList[0]

    try:
        last_messages = client.fetchThreadMessages(friend.uid) # 10000 should cover all messages
        last_messages.reverse()  # messages come in reversed order
    except KeyError:
        return []

    you_messages = []
    friend_messages = []

    for message in last_messages:
        if hasattr(message, 'text') and message.text:
            if message.author == str(os.environ['ID']):
                you_messages.append(message.text)
            else:
                friend_messages.append(message.text)

    print(you_messages)

    return (you_messages, friend_messages)
