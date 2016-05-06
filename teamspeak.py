import json
import os.path
import telnetlib


def get_json_file(file_name):
    if not os.path.isfile(file_name):
        open(file_name, 'w').write("{}")

    return json.loads(open(file_name).read())


def set_json_file(file_name, json_arr, indents):
    if indents:
        indents = 2
    else:
        indents = None

    return open(file_name, 'w').write(json.dumps(json_arr, indent=indents))


def rchop(thestring, ending):
    if thestring.endswith(ending):
        return thestring[:-len(ending)]
    return thestring


def send_command(tn, command):
    # This function clearly demonstrates my incredibly evident faith in self documenting code
    tn.write((command + "\n").encode('ascii'))

    message = ""
    while ("error id=" not in message) and ("msg=" not in message):
        message += tn.read_until(b"\n\r").decode('ascii')

    return message[:message.index("error id=")]
    # return rchop(rchop(tn.read_until(b"error id=0 msg=ok\n\r").decode('ascii'), "error id=0 msg=ok\n\r"), "\n\r")


def connect(host, queryport, port, user, password):
    tn = telnetlib.Telnet(host, queryport)

    buf = tn.read_until(b"command.\n\r")
    buf = login(tn, user, password)
    buf = use_port(tn, port)
    # send_command(tn, "login client_login_name=" + user + " client_login_password=" + password)
    # send_command(tn, "use port=" + port)
    send_command(tn, "clientupdate client_nickname=EvilAutoModerator")

    return tn

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
    bans = []
    banlist = send_command(tn, "banlist")
    banlist = banlist.split("|")

    for ban_listing in banlist:
        ban_listing = ban_listing.split(" ")
        ban = {}

        for ban_info in ban_listing:
            if "=" in ban_info:
                ban_info = ban_info.split("=")
                ban[ban_info[0]] = ban_info[1]
            else:
                ban[ban_info] = None

        bans.append(ban)

    return bans


def binding_list(tn):
    return send_command(tn, "bindinglist")

def channel_list(tn):
    return send_command