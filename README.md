##ss.conf for Surge!
This is a conf file for Surge!

In order to use Shadowsocks in Surge.

> `ssconf.py` can generate both gfwlist and whitelist, 
and auto update, 
whitelist is too long for iOS now, only Surge Mac can read.

##Proxy list 
Proxy list is generate from gfwlist, all marked with `force-remote-dns`.

White list come from [GFW Domain White List](https://goo.gl/tBixve).

##Anti ads
Ad's list come from [iyee/main.conf](https://goo.gl/70DG6i).


##How to use
Just use `gfwlist.conf` or `whitelist.conf` directly. Both in `configFileHere` directory!

>Or use `ssconf.py` to generate config file.


###Note:
Make sure edit `ServerConfig.txt` first to add your server infomation!

change your ss server config, like server ip, server port, and your password.

    [Proxy]
    💊DIRECT = direct
    🇭🇰HK = custom,your-server-here,your-port-here,aes-256-cfb,your-password-here,https://github.com/R0uter/ss.conf-for-surge/raw/master/ss.module
    🇸🇬SG = custom,your-server-here,your-port-here,aes-256-cfb,your-password-here,https://github.com/R0uter/ss.conf-for-surge/raw/master/ss.module
    🇯🇵JP = custom,your-server-here,your-port-here,aes-256-cfb,your-password-here,https://github.com/R0uter/ss.conf-for-surge/raw/master/ss.module
    🇺🇸US = custom,your-server-here,your-port-here,aes-256-cfb,your-password-here,https://github.com/R0uter/ss.conf-for-surge/raw/master/ss.module
    
    [Proxy Group]
    Proxy = select,💊DIRECT,🇭🇰HK,🇸🇬SG,🇯🇵JP,🇺🇸US

##MIT License (MIT)

The MIT License (MIT)

Copyright (c) 2015-2016 R0uter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

