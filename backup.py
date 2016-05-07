import sys
import telnetlib
import teamspeak
import time

timestamp = round(time.time())
backup_data = {}
config = teamspeak.get_json_file("configprelude.json")
tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"], "TSBackup")

# Server Info
if config["backup"]["server_info"]["backup"]:
    server_info = teamspeak.server_info(tn)
    used_server_info = {}

    for info_bit in server_info:
        if info_bit in config["backup"]["server_info"]["includes"]:
            used_server_info[info_bit] = server_info[info_bit]

    backup_data["server"] = used_server_info

# Channels
if config["backup"]["channels"]["backup"]:
    backup_data["channels"] = teamspeak.channel_list(tn)

# Bans
if config["backup"]["bans"]["backup"]:
    backup_data["bans"] = teamspeak.ban_list(tn)

# Server Groups
if config["backup"]["server_groups"]["backup"]:
    server_groups = teamspeak.server_group_list(tn)
    for server_group in server_groups:
        server_group["permissions"] = teamspeak.server_group_permission_list(tn, server_group["sgid"], config["json"]["use_permission_string_ids"])

    backup_data["server_groups"] = server_groups

# Channel Groups
if config["backup"]["channel_groups"]["backup"]:
    channel_groups = teamspeak.channel_group_list(tn)
    for channel_group in channel_groups:
        channel_group["permissions"] = teamspeak.channel_group_permission_list(tn, channel_group["cgid"], config["json"]["use_permission_string_ids"])

    backup_data["channel_groups"] = channel_groups

file = teamspeak.set_json_file("backup-" + str(timestamp) + ".json", backup_data, config["json"]["use_file_indentation"])
teamspeak.quit(tn)
tn.close()
