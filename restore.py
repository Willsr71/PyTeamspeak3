import sys
import time
import telnetlib
import teamspeak

if len(sys.argv) != 2:
    print("Usage: python restore.py <backup file>")
    sys.exit(1)

config = teamspeak.get_json_file("configprelude.json")
tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"], "TSBackup")

backup_data = teamspeak.get_json_file(sys.argv[1])

# Server Info
try:
    for server_info_bit in backup_data["server"]:
        if backup_data["server"][server_info_bit] is not None:
            teamspeak.server_edit(tn, {server_info_bit: backup_data["server"][server_info_bit]})
except AttributeError:
    print("No server info backup data found, skipping...")

# Channels
try:
    old_channels = teamspeak.channel_list(tn)

    teamspeak.channel_create(tn, "Temporary channel " + time.time(), {"channel_flag_default": "1"})

    for channel in old_channels:
        teamspeak.channel_delete(tn, channel["cid"], True)

    for channel in backup_data["channels"]:
        channel_name = channel["channel_name"]
        del channel["channel_name"]
        buf = teamspeak.channel_create(tn, channel_name, channel)
        cid = teamspeak.parse_objects(buf)
        print(cid)

except AttributeError:
    print("No channels backup data found, skipping...")

# Bans
try:
    backup_data["bans"]
except AttributeError:
    print("No bans backup data found, skipping...")

# Server Groups
try:
    backup_data["server_groups"]
except AttributeError:
    print("No server groups backup data found, skipping...")

# Channel Groups
try:
    backup_data["channel_groups"]
except AttributeError:
    print("No channel groups backup data found, skipping...")

teamspeak.quit(tn)
tn.close()
