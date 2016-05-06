import sys
import telnetlib
import teamspeak
import time

timestamp = round(time.time())
backup_data = {}
config = teamspeak.get_json_file("configenjin.json")
tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"], "TSBackup")

# buf = teamspeak.send_command(tn, "help")
# print(buf)

backup_data["instance"] = None
backup_data["channels"] = None
backup_data["bans"] = teamspeak.ban_list(tn)
backup_data["server_groups"] = None
backup_data["channel_groups"] = None

file = teamspeak.set_json_file("backup-" + str(timestamp) + ".json", backup_data, config["json_file_indents"])
teamspeak.quit(tn)
tn.close()
