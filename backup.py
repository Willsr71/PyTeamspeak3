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

bans = teamspeak.ban_list(tn)
print(bans)

# file = teamspeak.set_json_file("backup-" + str(timestamp) + ".json", backup_data)
teamspeak.quit(tn)
tn.close()
