import sys
import time
import telnetlib
import teamspeak

if len(sys.argv) != 2:
    print("Usage: python restore.py <backup file>")
    sys.exit(1)

timestamp = time.time()

config = teamspeak.get_json_file("configprelude.json")
tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"], "TSBackup")

teamspeak.send_text_message(tn, 3, 1, "Restoring server from backup...")
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

    buf = teamspeak.channel_create(tn, "Temporary\schannel\s" + str(time.time()), {"channel_flag_permanent": "1", "channel_flag_default": "1"})
    temp_channel = teamspeak.parse_objects(buf)["cid"]

    for channel in old_channels:
        if channel["pid"] == "0":
            teamspeak.channel_delete(tn, channel["cid"], True)

    for channel in backup_data["channels"]:
        channel_name = channel["channel_name"]
        channel_permissions = channel["permissions"]
        old_cid = channel["cid"]

        del channel["channel_name"]
        del channel["permissions"]
        del channel["cid"]

        buf = teamspeak.channel_create(tn, channel_name, channel)
        channel_data = teamspeak.parse_objects(buf)

        if "cid" not in channel_data:
            continue

        cid = int(channel_data["cid"])

        for channel_permission in channel_permissions:
            if "cid" in channel_permission:
                channel_permission["cid"] = channel_data["cid"]

        teamspeak.channel_add_permission(tn, channel_data["cid"], channel_permissions)

        for c in backup_data["channels"]:
            if "cid" not in c:
                continue

            if old_cid == c["channel_order"]:
                c["channel_order"] = cid

            if old_cid == c["cpid"]:
                c["cpid"] = cid

    teamspeak.channel_delete(tn, temp_channel, True)


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

teamspeak.send_text_message(tn, 3, 1, "Done. Restore took " + str(time.time() - timestamp) + " seconds")
teamspeak.quit(tn)
tn.close()

finished_timestamp = time.time()
print("Restore took", finished_timestamp - timestamp, "seconds")
