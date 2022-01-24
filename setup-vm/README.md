# setup-vm
---
Shell Scripts to setup and configure Virtual Machines

Create diagram :
 - maintain a `.drawio` file
 - attach the image to be showcased in the `README.md`

node.js support :
 - add node.js support for webservers

Error Handling :
 - check Internet connectivity
 - validate if command is executed properly
 - what happens if script crashes in between

User Add :
 - User add logic still not implemented

Credential :
 - there are scopes where credentials might get exposed during `User Add`

Decouple instances from logic :
 - maybe maintain separate config file to specify instances
 - should be flexible for multiple setups

Try to use VagrantFile :
 - go for `geerlingguy` `focal`
 - also look into alternatives
