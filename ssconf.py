#!/usr/bin/env python  
#coding=utf-8
#  https://www.logcg.com
#
#

import urllib2 
import re
import os
import datetime
import base64
import shutil


#Your SS IP or Domain here
server = '127.0.0.1'
#Your SS port
port = '1080'
#Your SS method
method = 'aes-256-cfb'
#Your SS password
passwd = 'your_password_here'


#---------------------------

def whiteListCheck():
    whitelist = './list/whitelist'
    wtfs = open(whitelist,'r')
    wfs = open('./list/whitelist.txt','w')
    
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'
    
    # Write list
    for line in wtfs.readlines():
        
        domain = re.findall(domain_pattern, line)
        if domain:
            try:
                found = domainlist.index(domain[0])
            except ValueError:
                domainlist.append(domain[0])
                wfs.write('DOMAIN-SUFFIX,%s,DIRECT\n'%(domain[0]))
        else:
            continue

    wtfs.close()
    wfs.close()

def subConfigGen(configName,file_content):
    content = file_content
    content = content.replace('__CONFIG__',configName)
    content = content.replace('__SERVER__', server)
    content = content.replace('__PORT__', port)
    content = content.replace('__METHOD__', method)
    content = content.replace('__PASSWORD__', passwd)
    return content


# the url of gfwlist
baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
# match comments/title/whitelist/ip address
comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'
tmpfile = './list/tmp'
outfile = './list/gfwlist.txt'

 
fs =  file(outfile, 'w')
fs.write('// SS config file for surge with gfw list \n')
fs.write('// updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
fs.write('\n')
 
print 'Fetching gfw list...'
try:
    content = urllib2.urlopen(baseurl, timeout=10).read().decode('base64')
     
    # write the decoded content to file then read line by line
    tfs = open(tmpfile, 'w')
    tfs.write(content)
    tfs.close()
    tfs = open(tmpfile, 'r')
    print 'GFW list fetched, writing...'
except:
    tfs = open(tmpfile, 'r')
    print 'GFW list fetch failed, use tmp instead...'
 

 
# Store all domains, deduplicate records
domainlist = []

# Write list
for line in tfs.readlines():
    
    if re.findall(comment_pattern, line):
        continue
    else:
        domain = re.findall(domain_pattern, line)
        if domain:
            try:
                found = domainlist.index(domain[0])
            except ValueError:
                domainlist.append(domain[0])
                fs.write('DOMAIN-SUFFIX,%s,Proxy,force-remote-dns\n'%(domain[0]))
        else:
            continue

tfs.close()
fs.close()

# get list to block most of ads .
# the url of  https://gist.github.com/iyee/2e27c124af2f7a4f0d5a
outfile = './list/adlist.txt'
tmpfile = './list/adtmp'
baseurl = 'https://gist.githubusercontent.com/iyee/2e27c124af2f7a4f0d5a/raw/6000aa7ad6189a5cc210f9653e11f1be6f637f4d/main.conf'

comment_pattern = '^\!|\[|^@@|\/|http|\#|\*|\?|\_|^\.|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '(\#?[\w\-\_]+\,[\/\w\.\-\_]+\,REJECT)[\/\*]*'

fs =  file(outfile, 'w')
fs.write('// thx  https://gist.github.com/iyee/2e27c124af2f7a4f0d5a \n')
fs.write('// updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
fs.write('\n')

print 'Fetching ad list...'
try:
    content = urllib2.urlopen(baseurl, timeout=10).read()
    
    # write the content to file then read line by line
    tfs = open(tmpfile, 'w')
    tfs.write(content)
    tfs.close()
    tfs = open(tmpfile, 'r')
    print 'adlist fetched, writing...'
except:
    tfs = open(tmpfile, 'r')
    print 'adlist fetch failed, use tmpfile instead...'
# Store all domains, deduplicate records
domainlist = []

# Write list
for line in tfs.readlines():
    
    if re.findall(comment_pattern, line):
        continue
    else:
        domain = re.findall(domain_pattern, line)
        if domain:
            try:
                found = domainlist.index(domain[0])
            except ValueError:
                domainlist.append(domain[0])
                fs.write(domain[0] + '\n')
        else:
            continue

tfs.close()
fs.close()





print 'Generate config file: gfwlist_main.conf'
cfs = open('template/ss_gfwlist_conf', 'r')
gfwlist = open('list/gfwlist.txt', 'r')
adlist = open('list/adlist.txt', 'r')
file_content = cfs.read()
adlist_buffer = adlist.read()
gfwlist_buffer = gfwlist.read()
gfwlist.close()
adlist.close()
cfs.close()

file_content = file_content.replace('__ADBLOCK__', adlist_buffer)
file_content = file_content.replace('__GFWLIST__', gfwlist_buffer)
file_content = file_content.replace('__SERVER__', server)
file_content = file_content.replace('__PORT__', port)
file_content = file_content.replace('__METHOD__', method)
file_content = file_content.replace('__PASSWORD__', passwd)

confs = open('configFileHere/gfwlist_main.conf', 'w')
confs.write(file_content)
confs.close()
# whitelist config
print 'Generate config file: whitelist_main.conf'
whiteListCheck()
cfs = open('template/ss_whitelist_conf', 'r')
gfwlist = open('list/whitelist.txt', 'r')
adlist = open('list/adlist.txt', 'r')
file_content = cfs.read()
adlist_buffer = adlist.read()
gfwlist_buffer = gfwlist.read()
gfwlist.close()
adlist.close()
cfs.close()

file_content = file_content.replace('__ADBLOCK__', adlist_buffer)
file_content = file_content.replace('__GFWWHITELIST__', gfwlist_buffer)
file_content = file_content.replace('__SERVER__', server)
file_content = file_content.replace('__PORT__', port)
file_content = file_content.replace('__METHOD__', method)
file_content = file_content.replace('__PASSWORD__', passwd)

confs = open('configFileHere/whitelist_main.conf', 'w')
confs.write(file_content)
confs.close()

print 'Generate sub-config file for whitelist_main.conf and gfwlist_main.conf'

fs = open('template/sub_conf', 'r')
sub_config = fs.read()
fs.close()
fs = open('configFileHere/whitelist_server.conf', 'w')
fs.write(subConfigGen('whitelist_main.conf',sub_config))
fs.close()
fs = open('configFileHere/gfwlist_server.conf', 'w')
fs.write(subConfigGen('gfwlist_main.conf',sub_config))
fs.close()




print 'All done!'
