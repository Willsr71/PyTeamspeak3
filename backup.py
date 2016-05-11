import sys
import telnetlib
import teamspeak
import time

timestamp = time.time()

backup_data = {}
config = teamspeak.get_json_file("configenjin.json")
tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"], "TSBackup")

teamspeak.send_text_message(tn, 3, 1, "Backing up server...")

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
    channels = teamspeak.channel_list(tn)

    for channel in channels:
        channel_info = teamspeak.parse_objects(teamspeak.channel_info(tn, channel["cid"]))
        for attribute in channel_info:
            channel[attribute] = channel_info[attribute]

        for excluded_attribute in config["backup"]["channels"]["excludes_attributes"]:
            del channel[excluded_attribute]

        for changed_attribute in config["backup"]["channels"]["changes_attributes"]:
            channel[changed_attribute["to"]] = channel[changed_attribute["from"]]
            del channel[changed_attribute["from"]]

        channel["permissions"] = teamspeak.channel_permission_list(tn, channel["cid"], config["json"]["use_permission_string_ids"])

    backup_data["channels"] = channels

# Bans
if config["backup"]["bans"]["backup"]:
    backup_data["bans"] = teamspeak.ban_list(tn)

# Server Groups
if config["backup"]["server_groups"]["backup"]:
    server_groups = teamspeak.server_group_list(tn)
    for server_group in server_groups:
        if server_group["sgid"] not in config["backup"]["server_groups"]["excludes"]:
            server_group["permissions"] = teamspeak.server_group_permission_list(tn, server_group["sgid"], config["json"]["use_permission_string_ids"])

    backup_data["server_groups"] = server_groups

# Channel Groups
if config["backup"]["channel_groups"]["backup"]:
    channel_groups = teamspeak.channel_group_list(tn)
    for channel_group in channel_groups:
        if channel_group["cgid"] not in config["backup"]["server_groups"]["excludes"]:
            channel_group["permissions"] = teamspeak.channel_group_permission_list(tn, channel_group["cgid"], config["json"]["use_permission_string_ids"])

    backup_data["channel_groups"] = channel_groups

file = teamspeak.set_json_file("backup-" + str(round(timestamp)) + ".json", backup_data, config["json"]["use_file_indentation"])

teamspeak.send_text_message(tn, 3, 1, "Done. Backup took " + str(time.time() - timestamp) + " seconds")
teamspeak.quit(tn)
tn.close()

finished_timestamp = time.time()
print("Backup took", finished_timestamp - timestamp, "seconds")
