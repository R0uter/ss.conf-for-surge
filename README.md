##ss.conf for Surge!
This is a conf file for Surge!

In order to use shad0ws0cks in Surge.

> `ssconf.py` can generate both gfwlist and whitelist, and auto update the gfwlist and adlist, whitelist's auto update function is not implement yet.

##Proxy list 
Proxy list was generated from gfwlist, all marked with `force-remote-dns`.

White list come from https://goo.gl/tBixve.

##Anti ads
Ad's list from https://goo.gl/70DG6i.


##How-to-use
Just use `gfwlist-ss.conf` or `whitelist-ss.conf` directly. Both in `ss.conf` directory!

>Or use `ssconf.py` to generate config file.

###Note:
Make sure edit `ssconf.py` or config file first!

change your ss server config, like server ip, server port, and your password.


    #Your SS IP or Domain here
    server = '127.0.0.1'
    #Your SS port
    port = '1080'
    #Your SS method
    method = 'aes-256-cfb'
    #Your SS password
    passwd = 'your_password_here'
