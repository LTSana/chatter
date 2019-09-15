import os
import time
import requests

from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_socketio import SocketIO, emit

# Custom packet
from chat_bot import bot

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

system_data = {"channel_names": []}
channel_storage = []

# Prevent Caching so CSS changes can take immediate effect
@app.after_request
def after_request(respose):
	respose.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	respose.headers["Expire"] = 0
	respose.headers["Pragma"] = "no-cache"
	return respose


@app.route("/")
def index():
	"""Show chatters channels"""
	return render_template("index.html", channel_list=system_data["channel_names"])


@app.route("/channel_name/<string:channel>", methods=["GET", "POST"])
def channel_name(channel):
	"""Load the apropriate channel page"""

	# Check if the channel exist in the available channel list
	if channel not in system_data["channel_names"]:
		print("Channel doesn't exist!")
		return redirect("/")

	# Store the Data to send to the HTML code in this variable
	channel_stored_chat_HTML = None

	# Check if there is any chat logs in the variable dictionary list
	if channel_storage:

		# Temporary variable for checks
		channel_present = False
		channel_present_n = None

		# Check to see if any of the dictionary list matches the channel being accesssed
		for alpha in range(len(channel_storage)):
			if channel in channel_storage[alpha]:
				channel_present = True
				channel_present_n = alpha

		# If the channel chat log exist in the logs add the chat log to the variable
		if channel_present:
			channel_stored_chat_HTML = channel_storage[channel_present_n][channel]

	return render_template("channel.html", channel_name=channel,
										   channel_stored_chat_HTML=channel_stored_chat_HTML)


@app.route("/login", methods=["POST"])
def login():
	""" Login """

	return redirect("/")


@app.route("/logout")
def logout():
	""" Remove username from LocalStorage on Javascript and reload the page"""

	return redirect("/")


@app.route("/refresh_channels", methods=["GET", "POST"])
def refresh_channels():
	"""Get new channel list"""

	return jsonify({"channel_list": system_data["channel_names"]})


@app.route("/create_channel", methods=["POST", "GET"])
def create_channel():
	"""Create a new channel"""

	creation_status = None
	new_channel = str(request.form.get("new_channel_name"))

	if new_channel not in system_data["channel_names"]:
		system_data["channel_names"].append(new_channel)
		creation_status = "GOOD"
	else:
		creation_status = "ALREADY"

	return jsonify({"CREATE_STATUS": creation_status})


@socketio.on("chatter")
def message_sender(data):
	"""Receive messages and send to the appropriate channel"""

	# Get the current time from the server
	time_msg = time.localtime()
	time_msg = str(time_msg.tm_mday) +"/"+ str(time_msg.tm_mon) +"/"+ str(time_msg.tm_year) +"-"+ str(time_msg.tm_hour) +":"+ str(time_msg.tm_min)

	# Store the chat log on the server. If the server is restarted the log will be cleared
	if channel_storage:
		channel_in_storage = False
		for alpha in range(len(channel_storage)):
			if data["channel_name"] in channel_storage[alpha]:
				channel_in_storage = True
				channel_in_section = alpha
		
		if channel_in_storage:
			channel_storage[channel_in_section][data["channel_name"]].append([{"timestamp": time_msg,
																			   "username": data["username_1"],
																			   "message": data["msg"]}])

			# If the chat for a channel is logger then 100. Delete the oldest message and only keep 100 messages
			if len(channel_storage[channel_in_section][data["channel_name"]]) >= 101:
				len(channel_storage[channel_in_section][data["channel_name"]].pop(0))
		else:
			channel_storage.append({data["channel_name"]: [[{"timestamp": time_msg,
															 "username": data["username_1"],
															 "message": data["msg"]}]]})
	else:
		channel_storage.append({data["channel_name"]: [[{"timestamp": time_msg,
														 "username": data["username_1"],
														 "message": data["msg"]}]]})

	# Emit the message to the proper channel
	emit(data["channel_name"], {"timestamp": time_msg, "msg": data["msg"], "username_1": data["username_1"]}, broadcast=True)

	# Check if the BOT is being activated
	if len(data["msg"]) >= 4:
		if str(data["msg"][:4]) == "@BOT":
			bot(data)


if __name__ == "__main__":
	socketio.run(app)