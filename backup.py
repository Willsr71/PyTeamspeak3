import sys
import telnetlib
import teamspeak
import time
from datetime import datetime

timestamp = round(time.time())
backup_data = {}
config = teamspeak.get_json_file("configenjin.json")
tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"])

# buf = teamspeak.send_command(tn, "help")
# print(buf)

# Bans

bans = []
ban_list = teamspeak.ban_list(tn).split("|")
for ban_listing in ban_list:
    ban_listing = ban_listing.split(" ")
    ban = {}

    for ban_info in ban_listing:
        if "=" in ban_info:
            ban_info = ban_info.split("=")
            ban[ban_info[0]] = ban_info[1]
        else:
            ban[ban_info] = None

    bans.append(ban)
backup_data["bans"] = bans

file = teamspeak.set_json_file("backup-" + str(timestamp) + ".json", backup_data)
teamspeak.quit(tn)
tn.close()
