# Chatter

This Project allows users to chat in channels using Javascript and Python 3.5+

## Home Page
In this page javascript will check if the user is using a username, if not it will prompt to enter a username to use.
User can see all the available channels on the server, with a refresh button to refresh the list.
Users will also have a recently visited list to see the channels they've visited in the past.
If a user needs to make a new channel, they can easily create a new one by clicking on the +Create Channel button and name it anything, as long as it doesn't conflict with other channel names.
From this page users can join any channel.

## Channel page
Users can chat with each other and ask the bot things (The bot is very very very simple).
The javascript will remember that the user is in the channel so if the tab is closed and they return it will send them to the channel they were still in.
The chat will be logged up to 100 messages on the server so when new users and previous users return they can see what has been going on in the channel.

## How to setup
0. `pip install -r requirements.txt`
1. `set FLASK_APP=application.py`
2. `set FLASK_ENV=development`
3. `set FLASK_DEBUG=1`
4. `set SECRET_KEY=klhakhgkjdfhglfkmkw3kl4jh54l3jkb234kn`
5. `python application.py`


Web Programming with Python and JavaScript
