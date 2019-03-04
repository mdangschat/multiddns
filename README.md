# Multi Dynamic DNS
Updates multiple DDNS entries at once.
My FritzBox router can only update a single DDNS entry.
Therefore I run this script on my (local) server, my FritzBox sends an update to my server, which
in turn updates multiple other DDNS entries.

## Security Notes
Currently the server does not provide any encryption, so do not use this over the internet! 
