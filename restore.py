import sys
import time
import util
import teamspeak
from util import print_line, colors

if len(sys.argv) != 2:
    print("Usage: python restore.py <backup file>")
    sys.exit(1)

print_line("> Loading config...")
config = util.get_json_file("config-beast.json")
print_line(colors.GREEN + " Done.\n" + colors.END)

print_line("> Loading backup file...")
backup_data = util.get_json_file(sys.argv[1])
print_line(colors.GREEN + " Done.\n" + colors.END)

print_line("> Connecting...")
tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"], "TSBackup")
print_line(colors.GREEN + " Done.\n" + colors.END)

if config["announce_messages"]:
    teamspeak.send_text_message(tn, 3, 1, "Restoring server from backup...")

start_timestamp = time.time()

# Server Info
print_line("> Restoring server info...")
if "server" in backup_data:
    poscounter = 0
    for server_info_bit in backup_data["server"]:
        poscounter += 1
        print_line("\r> Restoring server info... " + colors.YELLOW + "(" + str(poscounter) + "/" + str(len(backup_data["server"])) + ")" + colors.END)

        if backup_data["server"][server_info_bit] is not None:
            teamspeak.server_edit(tn, {server_info_bit: backup_data["server"][server_info_bit]})

    print_line(colors.GREEN + " Done.\n" + colors.END)
else:
    print_line(colors.YELLOW + " Skipped.\n" + colors.END)

# Server Groups
print_line("> Restoring server groups...")
if "server_groups" in backup_data:

    buf = teamspeak.permission_reset(tn)
    util.set_json_file("token.json", buf, True)

    # temporary method of doing this.
    time.sleep(10)
    tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"], "TSBackup")

    poscounter = 0
    for server_group in backup_data["server_groups"]:
        poscounter += 1
        print_line("\r> Restoring server groups... " + colors.YELLOW + "(" + str(poscounter) + "/" + str(len(backup_data["server_groups"])) + ")" + colors.END)

        if server_group["sgid"] in config["backup"]["server_groups"]["excludes"]:
            continue

        teamspeak.server_group_add(tn, server_group["name"], 1)

    print_line(colors.GREEN + " Done.\n" + colors.END)
else:
    print_line(colors.YELLOW + " Skipped.\n" + colors.END)

# Channel Groups
print_line("> Restoring channel groups...")
if "channel_groups" in backup_data:
    print_line(colors.GREEN + " Done.\n" + colors.END)
else:
    print_line(colors.YELLOW + " Skipped.\n" + colors.END)

# Channels
print_line("> Restoring channels...")
if "channels" in backup_data:
    old_channels = teamspeak.channel_list(tn)

    buf = teamspeak.channel_create(tn, "Temporary\schannel\s" + str(round(start_timestamp)), {"channel_flag_permanent": "1", "channel_flag_default": "1"})
    temp_channel = buf["cid"]

    poscounter = 0
    for channel in old_channels:
        poscounter += 1
        print_line("\r> Deleting old channels... " + colors.YELLOW + "(" + str(poscounter) + "/" + str(len(old_channels)) + ")" + colors.END)

        if channel["pid"] == "0":
            teamspeak.channel_delete(tn, channel["cid"], True)

    print_line(colors.GREEN + " Done.\n" + colors.END)

    poscounter = 0
    for channel in backup_data["channels"]:
        poscounter += 1
        print_line("\r> Restoring channels... " + colors.YELLOW + "(" + str(poscounter) + "/" + str(len(backup_data["channels"])) + ")" + colors.END)

        channel_name = channel["channel_name"]
        channel_permissions = channel["permissions"]
        old_cid = channel["cid"]

        del channel["channel_name"]
        del channel["permissions"]
        del channel["cid"]

        channel_data = teamspeak.channel_create(tn, channel_name, channel)

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

    print_line(colors.GREEN + " Done.\n" + colors.END)
else:
    print_line(colors.YELLOW + " Skipped.\n" + colors.END)

# Bans
print_line("> Restoring bans...")
if "bans" in backup_data:
    print_line("\r> Deleting old bans...")
    teamspeak.ban_delete_all(tn)
    print_line(colors.GREEN + " Done.\n" + colors.END)

    poscounter = 0
    for ban in backup_data["bans"]:
        poscounter += 1
        print_line("\r> Restoring bans... " + colors.YELLOW + "(" + str(poscounter) + "/" + str(len(backup_data["bans"])) + ")" + colors.END)

        teamspeak.ban_add(tn, ban["ip"], ban["name"], ban["uid"], ban["duration"], ban["reason"])

    print_line(colors.GREEN + " Done.\n" + colors.END)
else:
    print_line(colors.YELLOW + " Skipped.\n" + colors.END)

finished_timestamp = time.time()
time_taken = round(finished_timestamp - start_timestamp, 3)

if config["announce_messages"]:
    teamspeak.send_text_message(tn, 3, 1, "Done. Restore took " + str(time_taken) + " seconds")

print_line("> Disconnecting...")
teamspeak.quit(tn)
tn.close()
print_line(colors.GREEN + " Done.\n" + colors.END)

print("\nRestore took " + str(time_taken) + " seconds")
