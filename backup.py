import sys
import telnetlib
import teamspeak
import time

timestamp = round(time.time())
backup_data = {}
config = teamspeak.get_json_file("configenjin.json")
tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"], "TSBackup")

# Server Info
backup_data["server"] = teamspeak.server_info(tn)

# Channels
backup_data["channels"] = teamspeak.channel_list(tn)

# Bans
backup_data["bans"] = teamspeak.ban_list(tn)

# Server Groups
server_groups = teamspeak.server_group_list(tn)
for server_group in server_groups:
    server_group["permissions"] = teamspeak.server_group_permission_list(tn, server_group["sgid"], config["use_permission_string_ids"])

backup_data["server_groups"] = server_groups

# Channel Groups
channel_groups = teamspeak.channel_group_list(tn)
for channel_group in channel_groups:
    channel_group["permissions"] = teamspeak.channel_group_permission_list(tn, channel_group["cgid"], config["use_permission_string_ids"])

backup_data["channel_groups"] = channel_groups

file = teamspeak.set_json_file("backup-" + str(timestamp) + ".json", backup_data, config["json_file_indents"])
teamspeak.quit(tn)
tn.close()
