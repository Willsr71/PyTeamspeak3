import sys
import time
import util
import teamspeak
from util import print_line, colors

if len(sys.argv) != 2:
    print("Usage: python addgroups.py <group file>")
    sys.exit(1)

print_line("> Loading Config...")
config = util.get_json_file("config-beast.json")
print_line(colors.GREEN + " Done.\n" + colors.END)

print_line("> Loading ranks file...")
group_data = util.get_json_file(sys.argv[1])
print_line(colors.GREEN + " Done.\n" + colors.END)

print_line("> Connecting...")
tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"], "RankAdder", rate_limited=config["rate_limited"])
print_line(colors.GREEN + " Done.\n" + colors.END)

if config["announce_messages"]:
    teamspeak.send_text_message(tn, 3, 1, "Creating Ranks...")

start_timestamp = time.time()

# Server Groups
print_line("> Adding server groups...")

existing_server_groups = {}
for existing_server_group in teamspeak.server_group_list(tn):
    existing_server_groups[existing_server_group["name"]] = {"sgid": existing_server_group["sgid"]}

poscounter = 0
for server_group in group_data["server_groups"]:
    poscounter += 1
    print_line("\r> Adding server groups... " + colors.YELLOW + "(" + str(poscounter) + "/" + str(len(group_data["server_groups"])) + ")" + colors.END)

    name = server_group["name"]

    if name in existing_server_groups:
        existing_server_groups[name]["clients"] = teamspeak.server_group_client_list(tn, existing_server_groups[name]["sgid"])
        teamspeak.server_group_delete(tn, existing_server_groups[name]["sgid"])

    server_group_id = teamspeak.server_group_add(tn, name, 1)
    print(server_group_id)
    server_group_id = server_group_id["sgid"]

    permissions = [{"permsid": "i_group_sort_id", "permvalue": server_group["sort"], "permnegated": 0, "permskip": 0},
                   {"permsid": "i_icon_id", "permvalue": 0, "permnegated": 0, "permskip": 0}]
    for permission in group_data["server_group_permissions"]:
        permissions.append({"permsid": permission, "permvalue": server_group["power"], "permnegated": 0, "permskip": 0})

    teamspeak.server_group_add_permissions(tn, server_group_id, permissions)

    if name in existing_server_groups:
        for client in existing_server_groups[name]["clients"]:
            teamspeak.server_group_add_client(tn, server_group_id, client["cldbid"])

print_line(colors.GREEN + " Done.\n" + colors.END)
