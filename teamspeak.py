import sys
import json
import os.path
import telnetlib


def get_json_file(file_name):
    try:
        return json.loads(open(file_name).read())
    except FileNotFoundError:
        print("File does not exist")
        sys.exit(1)


def set_json_file(file_name, json_arr, indents):
    if indents:
        indents = 2
    else:
        indents = None

    return open(file_name, 'w').write(json.dumps(json_arr, indent=indents))


def send_command(tn, command):
    tn.write((command + "\n").encode('ascii'))

    message = ""
    while ("error id=" not in message) and ("msg=" not in message):
        message += tn.read_until(b"\n\r").decode('ascii')

    # Because of some rare cases
    message = message.replace("\n\r", "")

    error_id = int(message[message.index("error id=") + 9:message.index("msg=") - 1])
    error_message = message[message.index("msg=") + 4:]

    # print(command)
    if not error_id == 0:
        print(command)
        print("error id=" + str(error_id) + " msg=" + error_message)

    return message[:message.index("error id=")]


def connect(host, queryport, port, user, password, nickname):
    tn = telnetlib.Telnet(host, queryport)

    tn.read_until(b"command.\n\r")
    login(tn, user, password)
    use_port(tn, port)
    send_command(tn, "clientupdate client_nickname=" + nickname)

    return tn


def parse_objects(sq_objects):
    json_objects = {}

    sq_objects = sq_objects.split(" ")
    for obj in sq_objects:
        if "=" in obj:
            obj = obj.split("=", 1)
            json_objects[obj[0]] = obj[1]
        else:
            json_objects[obj] = None

    return json_objects


def parse_list(sq_list):
    json_list = []

    sq_list = sq_list.split("|")
    for item in sq_list:
        json_list.append(item)

    return json_list


def deparse_objects(json_objects):
    sq_objects = ""

    for json_object in json_objects:
        if json_objects[json_object] is not None:
            sq_objects += " " + json_object + "=" + json_objects[json_object]

    return sq_objects


###############################
#                             #
#  Teamspeak Query functions  #
#                             #
###############################


def login(tn, username, password):
    return send_command(tn, "login client_login_name=" + username + " client_login_password=" + password)


def logout(tn):
    return send_command(tn, "logout")


def quit(tn):
    return send_command(tn, "quit")


def use_port(tn, port):
    return send_command(tn, "use port=" + port)


def ban_add(tn, ip_regex=None, name_regex=None, uid_regex=None, time_in_seconds=None, ban_reason=None):
    command_string = ""

    if not ip_regex is None:
        command_string += " ip=" + ip_regex
    if not name_regex is None:
        command_string += " name=" + name_regex
    if not uid_regex is None:
        command_string += " uid=" + uid_regex
    if not time_in_seconds is None:
        command_string += " time=" + time_in_seconds
    if not ban_reason is None:
        command_string += " banreason=" + ban_reason

    return send_command(tn, "banadd" + command_string)


def ban_client(tn, client_id, time_in_seconds=None, ban_reason=None):
    command_string = "clid=" + client_id
    if not time_in_seconds is None:
        command_string += " time=" + time_in_seconds
    if not ban_reason is None:
        command_string += "banreason" + ban_reason

    return send_command(tn, "banclient" + command_string)


def ban_delete_all(tn):
    return send_command(tn, "bandelall")


def ban_delete(tn, ban_id):
    return send_command(tn, "bandel banid=" + ban_id)


def ban_list(tn):
    ban_listings = parse_list(send_command(tn, "banlist"))

    bans = []
    for ban_listing in ban_listings:
        bans.append(parse_objects(ban_listing))

    return bans


def binding_list(tn):
    return send_command(tn, "bindinglist")


def channel_create(tn, channel_name, paramaters={}):
    return send_command(tn, "channelcreate channel_name=" + channel_name + deparse_objects(paramaters))


def channel_delete(tn, channel_id, force_delete=True):
    if force_delete:
        force_delete = "1"
    else:
        force_delete = "0"

    send_command(tn, "channeldelete cid=" + channel_id + " force=" + force_delete)


def channel_group_list(tn):
    channel_listings = parse_list(send_command(tn, "channelgrouplist"))

    groups = []
    for channel_listing in channel_listings:
        groups.append(parse_objects(channel_listing))

    return groups


def channel_group_permission_list(tn, channel_group_id, use_string_id=True):
    if use_string_id:
        use_string_id = " -permsid"
    else:
        use_string_id = ""

    permission_listings = parse_list(send_command(tn, "channelgrouppermlist cgid=" + channel_group_id + use_string_id))

    permissions = []
    for permission_listing in permission_listings:
        permissions.append(parse_objects(permission_listing))

    return permissions


def channel_list(tn):
    channel_listings = parse_list(send_command(tn, "channellist"))

    channels = []
    for channel_listing in channel_listings:
        channels.append(parse_objects(channel_listing))

    return channels


def server_edit(tn, paramaters):
    return send_command(tn, "serveredit" + deparse_objects(paramaters))


def server_group_list(tn):
    group_listings = parse_list(send_command(tn, "servergrouplist"))

    groups = []
    for group_listing in group_listings:
        groups.append(parse_objects(group_listing))

    return groups


def server_group_permission_list(tn, server_group_id, use_string_id=True):
    if use_string_id:
        use_string_id = " -permsid"
    else:
        use_string_id = ""

    permission_listings = parse_list(send_command(tn, "servergrouppermlist sgid=" + server_group_id + use_string_id))

    permissions = []
    for permission_listing in permission_listings:
        permissions.append(parse_objects(permission_listing))

    return permissions


def server_info(tn):
    return parse_objects(send_command(tn, "serverinfo"))
