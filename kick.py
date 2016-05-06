import sys
import telnetlib
import teamspeak


def get_client_by_name(username):
    for client in clients:
        if client["client_nickname"] == username:
            return client

config = teamspeak.get_json_file("configenjin.json")
tn = teamspeak.connect(config["host"], config["queryport"], config["port"], config["user"], config["password"], "EvilAutoModerator")
clients = []

clientsarr = teamspeak.send_command(tn, "clientlist")
clientsarr = clientsarr.split("|")
for clientarr in clientsarr:
    clientarr = clientarr.split(" ")

    client = {}
    for bit in clientarr:
        bit = bit.split("=")
        client[bit[0]] = bit[1]

    clients.append(client)

buf = teamspeak.send_command(tn, "clientkick reasonid=4 reasonmsg=Die\shuman. clid=" + get_client_by_name(sys.argv[1])["clid"])

teamspeak.quit(tn)
tn.close()