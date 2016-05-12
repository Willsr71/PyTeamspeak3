import sys
import telnetlib
import teamspeak
import time
from util import print_line, colors

backup_data = {}

print_line("> Loading Config...")
config = teamspeak.get_json_file("configenjin.json")
print_line(colors.GREEN + " Done.\n" + colors.END)

print_line("> Connecting...")
tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"], "TSBackup")
print_line(colors.GREEN + " Done.\n" + colors.END)

if config["announce_messages"]:
    teamspeak.send_text_message(tn, 3, 1, "Backing up server...")

start_timestamp = time.time()

# Server Info
print_line("> Backing up server info...")
if config["backup"]["server_info"]["backup"]:
    server_info = teamspeak.server_info(tn)
    used_server_info = {}

    poscounter = 0
    for info_bit in server_info:
        poscounter += 1
        print_line("\r> Backing up server info... " + colors.YELLOW + "(" + str(poscounter) + "/" + str(len(server_info)) + ")" + colors.END)

        if info_bit in config["backup"]["server_info"]["includes"]:
            used_server_info[info_bit] = server_info[info_bit]

    backup_data["server"] = used_server_info

    print_line(colors.GREEN + " Done.\n" + colors.END)
else:
    print_line(colors.YELLOW + " Skipped.\n" + colors.END)

# Server Groups
print_line("> Backing up server groups...")
if config["backup"]["server_groups"]["backup"]:
    server_groups = teamspeak.server_group_list(tn)

    poscounter = 0
    for server_group in server_groups:
        poscounter += 1
        print_line("\r> Backing up server groups... " + colors.YELLOW + "(" + str(poscounter) + "/" + str(len(server_groups)) + ")" + colors.END)

        if server_group["sgid"] in config["backup"]["server_groups"]["excludes"]:
            continue

        server_group["permissions"] = teamspeak.server_group_permission_list(tn, server_group["sgid"], config["json"]["use_permission_string_ids"])

    backup_data["server_groups"] = server_groups

    print_line(colors.GREEN + " Done.\n" + colors.END)
else:
    print_line(colors.YELLOW + " Skipped.\n" + colors.END)

# Channel Groups
print_line("> Backing up channel groups...")
if config["backup"]["channel_groups"]["backup"]:
    channel_groups = teamspeak.channel_group_list(tn)

    poscounter = 0
    for channel_group in channel_groups:
        poscounter += 1
        print_line("\r> Backing up channel groups... " + colors.YELLOW + "(" + str(poscounter) + "/" + str(len(channel_groups)) + ")" + colors.END)

        if channel_group["cgid"] in config["backup"]["server_groups"]["excludes"]:
            continue

        channel_group["permissions"] = teamspeak.channel_group_permission_list(tn, channel_group["cgid"], config["json"]["use_permission_string_ids"])

    backup_data["channel_groups"] = channel_groups

    print_line(colors.GREEN + " Done.\n" + colors.END)
else:
    print_line(colors.YELLOW + " Skipped.\n" + colors.END)

# Channels
print_line("> Backing up channels...")
if config["backup"]["channels"]["backup"]:
    channels = teamspeak.channel_list(tn)

    poscounter = 0
    for channel in channels:
        poscounter += 1
        print_line("\r> Backing up channels... " + colors.YELLOW + "(" + str(poscounter) + "/" + str(len(channels)) + ")" + colors.END)

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

    print_line(colors.GREEN + " Done.\n" + colors.END)
else:
    print_line(colors.YELLOW + " Skipped.\n" + colors.END)

# Bans
print_line("> Backing up bans...")
if config["backup"]["bans"]["backup"]:
    bans = teamspeak.ban_list(tn)

    poscounter = 0
    for ban in bans:
        poscounter += 1
        print_line("\r> Backing up bans... " + colors.YELLOW + "(" + str(poscounter) + "/" + str(len(bans)) + ")" + colors.END)

        for excluded_attribute in config["backup"]["bans"]["excludes_attributes"]:
            del ban[excluded_attribute]

    backup_data["bans"] = bans

    print_line(colors.GREEN + " Done.\n" + colors.END)
else:
    print_line(colors.YELLOW + " Skipped.\n" + colors.END)

file = teamspeak.set_json_file("backup-" + str(round(start_timestamp)) + ".json", backup_data, config["json"]["use_file_indentation"])

finished_timestamp = time.time()
time_taken = round(finished_timestamp - start_timestamp, 3)

if config["announce_messages"]:
    teamspeak.send_text_message(tn, 3, 1, "Done. Backup took " + str(time_taken) + " seconds")

print_line("> Disconnecting...")
teamspeak.quit(tn)
tn.close()
print_line(colors.GREEN + " Done.\n" + colors.END)

print("\nBackup took " + str(time_taken) + " seconds")
