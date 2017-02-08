import time
import telnetlib
from util import colors

rate_limiting = False
permissions = []


def send_command(tn, command):
    if rate_limiting:
        time.sleep(0.4)

    tn.write((command + "\n").encode('ascii'))

    message = ""
    while ("error id=" not in message) and ("msg=" not in message):
        message += tn.read_until(b"\n\r").decode('ascii')

    # Because of some rare cases
    message = message.replace("\n\r", "")

    status = parse_objects(message[message.index("error id="):])

    # print(command)
    if not status["error_id"] == "0":
        print("\n" + colors.RED)
        print(command)
        print(status)

        if "failed_permid" in status:
            for permission in permissions:
                if permission["permid"] == status["failed_permid"]:
                    print(permission["permid"] + "=" + permission["permname"])

        print(colors.END + "\n")

    # return message
    return message[:message.index("error id=")]


def connect(host, queryport, port, user, password, nickname, rate_limited=False):
    global rate_limiting, permissions

    rate_limiting = rate_limited
    tn = telnetlib.Telnet(host, queryport)

    tn.read_until(b"command.\n\r")
    login(tn, user, password)

    use_server_id(tn, port)
    use_port(tn, port)

    send_command(tn, "clientupdate client_nickname=" + nickname)
    permissions = permission_list(tn)

    return tn


def parse_objects(sq_objects):
    json_objects = {}

    sq_objects = sq_objects.split(" ")
    for x in range(0, len(sq_objects) - 1):
        if sq_objects[x] == "error" and "id=" in sq_objects[x + 1]:
            sq_objects[x] = sq_objects[x] + "_" + sq_objects[x + 1]
            sq_objects.pop(x + 1)

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

    if json_list[0] == '':
        json_list = []

    return json_list


def parse_object_list(sq_object_list):
    sq_objects = parse_list(sq_object_list)
    json_objects = []

    for sq_object in sq_objects:
        json_objects.append(parse_objects(sq_object))

    return json_objects


def deparse_objects(json_objects):
    sq_objects = ""

    for json_object in json_objects:
        if json_objects[json_object] is not None:
            sq_objects += " " + json_object + "=" + str(json_objects[json_object])

    return sq_objects


def deparse_object_list(json_list):
    sq_list = ""

    for json_object in json_list:
        sq_list += deparse_objects(json_object)[1:] + "|"

    sq_list = sq_list[:-1]

    return sq_list


###############################
#                             #
#  Teamspeak Query functions  #
#                             #
###############################


def login(tn, username, password):
    return parse_objects(send_command(tn, "login client_login_name=" + username + " client_login_password=" + password))


def logout(tn):
    return parse_objects(send_command(tn, "logout"))


def quit(tn):
    return parse_objects(send_command(tn, "quit"))


def use_server_id(tn, server_id):
    return parse_objects(send_command(tn, "use sid=" + server_id))


def use_port(tn, port):
    return parse_objects(send_command(tn, "use port=" + port))


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

    return parse_objects(send_command(tn, "banadd" + command_string))


def ban_client(tn, client_id, time_in_seconds=None, ban_reason=None):
    command_string = "clid=" + client_id
    if not time_in_seconds is None:
        command_string += " time=" + time_in_seconds
    if not ban_reason is None:
        command_string += "banreason" + ban_reason

    return parse_objects(send_command(tn, "banclient" + command_string))


def ban_delete_all(tn):
    return parse_objects(send_command(tn, "bandelall"))


def ban_delete(tn, ban_id):
    return parse_objects(send_command(tn, "bandel banid=" + ban_id))


def ban_list(tn):
    return parse_object_list(send_command(tn, "banlist"))


def channel_add_permission(tn, channel_id, channel_permissions):
    return parse_objects(send_command(tn, "channeladdperm cid=" + channel_id + " " + deparse_object_list(channel_permissions)))


def channel_create(tn, channel_name, paramaters={}):
    return parse_objects(send_command(tn, "channelcreate channel_name=" + channel_name + deparse_objects(paramaters)))


def channel_delete(tn, channel_id, force_delete=True):
    if force_delete:
        force_delete = "1"
    else:
        force_delete = "0"

    return parse_objects(send_command(tn, "channeldelete cid=" + channel_id + " force=" + force_delete))


def channel_group_list(tn):
    return parse_object_list(send_command(tn, "channelgrouplist"))


def channel_group_permission_list(tn, channel_group_id, use_string_id=True):
    if use_string_id:
        use_string_id = " -permsid"
    else:
        use_string_id = ""

    return parse_object_list(send_command(tn, "channelgrouppermlist cgid=" + channel_group_id + use_string_id))


def channel_list(tn):
    return parse_object_list(send_command(tn, "channellist"))


def channel_info(tn, channel_id):
    return send_command(tn, "channelinfo cid=" + channel_id)


def channel_permission_list(tn, channel_id, use_string_id):
    if use_string_id:
        use_string_id = " -permsid"
    else:
        use_string_id = ""

    return parse_object_list(send_command(tn, "channelpermlist cid=" + channel_id + use_string_id))


def permission_list(tn):
    return parse_object_list(send_command(tn, "permissionlist"))


def permission_reset(tn):
    return parse_objects(send_command(tn, "permreset"))


def send_text_message(tn, target_mode, target, message):
    message = message.replace(" ", "\s")
    return send_command(tn, "sendtextmessage targetmode=" + str(target_mode) + " target=" + str(target) + " msg=" + message)


def server_edit(tn, paramaters):
    return send_command(tn, "serveredit" + deparse_objects(paramaters))


def server_group_add(tn, group_name, group_type=1):
    return parse_objects(send_command(tn, "servergroupadd name=" + group_name + " type=" + str(group_type)))


def server_group_add_client(tn, server_group_id, client_id):
    return send_command(tn, "servergroupaddclient sgid=" + server_group_id + " cldbid=" + client_id)


def server_group_add_permissions(tn, server_group_id, server_group_permissions):
    return parse_objects(send_command(tn, "servergroupaddperm sgid=" + server_group_id + " " + deparse_object_list(server_group_permissions)))


def server_group_client_list(tn, server_group_id):
    return parse_object_list(send_command(tn, "servergroupclientlist sgid=" + server_group_id))


def server_group_copy(tn, source_group_id, target_group_id, group_name, group_type=1):
    return parse_objects(send_command(tn, "servergroupcopy ssgid=" + source_group_id + " tsgid=" + target_group_id + " name=" + group_name + " type=" + str(group_type)))


def server_group_delete(tn, server_group_id, force_delete=True):
    if force_delete:
        force_delete = "1"
    else:
        force_delete = "0"

    return parse_objects(send_command(tn, "servergroupdel sgid=" + server_group_id + " force=" + force_delete))


def server_group_list(tn):
    return parse_object_list(send_command(tn, "servergrouplist"))


def server_group_permission_list(tn, server_group_id, use_string_id=True):
    if use_string_id:
        use_string_id = " -permsid"
    else:
        use_string_id = ""

    return parse_object_list(send_command(tn, "servergrouppermlist sgid=" + server_group_id + use_string_id))


def server_info(tn):
    return parse_objects(send_command(tn, "serverinfo"))


def token_use(tn, token):
    return parse_objects(send_command(tn, "tokenuse token=" + token))
