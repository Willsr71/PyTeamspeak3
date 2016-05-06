# TeamspeakUtilities
A variety of Python utilities for TeamSpeak ServerQuery

# Current Features
- TeamSpeak API - an api that utilizes the serverquery api that utilizes the teamspeak api
- Server backup - script that backs up everything on your server to a json file
- Server restore - script that deletes everything on your server and restores it from a specified json file
- Kick user - mostly for testing various things. Usage: python kick.py <username>

# Config
|Option|Description|
|---|---|
|host|Server IP|
|queryport|ServerQuery port. Default is 10011|
|port|TeamSpeak port. Default is 9987|
|user|ServerQuery user. Must have permissions|
|password|ServerQuery user password|
|backup_server_info|Whether to backup server info|
|backup_channels|Whether to backup channels|
|backup_bans|Whether to backup bans|
|backup_server_groups|Whether to backup server groups|
|backup_channel_groups|Whether to backup channel groups|
|use_file_indentation|Whether to indent the output file or not|
|use_permission_string_ids|Whether to use string ids for permissions instead or numeric ids|