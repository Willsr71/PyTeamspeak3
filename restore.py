import sys
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
        buf = teamspeak.server_edit(tn, {server_info_bit: backup_data["server"][server_info_bit]})
    # print(buf)
except AttributeError:
    print("fuck")
    var = None

# Channels
if hasattr(backup_data, "channels"):
    backup_data["channels"]

# Bans
if hasattr(backup_data, "bans"):
    backup_data["bans"]

# Server Groups
if hasattr(backup_data, "server_groups"):
    backup_data["server_groups"]

# Channel Groups
if hasattr(backup_data, "channel_groups"):
    backup_data["channel_groups"]

teamspeak.quit(tn)
tn.close()
