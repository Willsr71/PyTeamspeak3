# PyTeamspeak3
Python API for Teamspeak ServerQuery. Includes backup and restore functions

# Features
- Python ServerQuery API
- Server backup (this includes server info, channels, bans, server groups, and channel groups)
- Server restore (everything listed above)

# Config
Bold options are ones that are most likely to need changing. Dashes represent a config section.

|Option|Default|Description|
|---|---|---|
|**host**|127.0.0.1|Server IP|
|**queryport**|10011|ServerQuery port|
|**port**|9987|Teamspeak server port|
|**user**|serveradmin|ServerQuery user. Must have permissions|
|**password**|null|ServerQuery user password|
|**announce_messages**|true|Whether to announce beginng and ending restores in Teamspeak global chat|
|backup-|||
|backup-server_info|||
|**backup-server_info-backup**|true|Whether to back up server info|
|backup-server_info-includes|\\a long list\\|What paramaters to include in the backup. These are better untouched.|
|backup-channels|||
|**backup-channels-backup**|true|Whether to back up channels|
|backup-channels-excludes|[]|What channels to exclude from the backup|
|backup-channels-excludes_attributes|\\a long list\\|What channel attributes to exclude from the backup|
|backup-channels-changes_attributes|pid -> cpid|What channel attributes to change the name of|
|backup-bans|||
|**backup-bans-backup**|true|Whether to back up bans|
|backup-bans-excludes_attributes|banid|What ban attributes to exclude from the backup|
|backup-server_groups|||
|**backup-server_groups-backup**|true|Whether to back up server groups|
|backup-server_groups-excludes|1, 2, 3, 4, 5|What server groups to exclude from the backup|
|backup-channel_groups|||
|**backup-channel_groups-backup**|true|Whether to back up channel groups|
|backup-channel_groups-excludes|1, 2, 3, 4, 5|What channel groups to exclude from the backup|
|json|||
|**json-use_file_indentation**|true|Whether to indent the backup file. This can increase file size drastically.|
|json-use_permission_string_ids|true|Whether to use string ids for the backup. This is highly recommended as numerical ids change every Teamspeak version.|
