#!/usr/bin/env python3
#coding=utf-8
#
#
#https://www.logcg.com

import urllib3
import re
import datetime
import certifi
import codecs


def getList(listUrl):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',  # Force certificate check.
        ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )

    data = http.request('GET', listUrl, timeout=10).data
    return data

def whiteListCheck():
    dnsmasq_china_list = 'https://github.com/R0uter/gfw_domain_whitelist/raw/master/whitelistCache'
    try:

        content = getList(dnsmasq_china_list)
        content = content.decode('utf-8')
        f = codecs.open('./list/whitelist', 'w', 'utf-8')
        f.write(content)
        f.close()
    except:
        print('Get list update failed,use cache to update instead.')

    whitelist = codecs.open('./list/whitelist','r','utf-8')
    whitelistTxt = codecs.open('./list/whitelist.txt','w','utf-8')
    whitelistTxt.write('// updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S" + '\n'))
    # Write list
    for line in whitelist.readlines():
        
        domain = re.findall(r'\w+\.\w+', line)
        if len(domain) > 0:
            whitelistTxt.write('DOMAIN-SUFFIX,%s,ChinaProxy\n'%(domain[0]))

    whitelist.close()
    whitelistTxt.close()



def getGfwList():
    # the url of gfwlist
    baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'

    comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    tmpfile = './list/tmp'

    gfwListTxt = codecs.open('./list/gfwlist.txt', 'w', 'utf-8')
    gfwListTxt.write('// SS config file for surge with gfw list \n')
    gfwListTxt.write('// updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    gfwListTxt.write('\n')

    try:

        data = getList(baseurl)

        content = codecs.decode(data, 'base64_codec').decode('utf-8')

        # write the decoded content to file then read line by line
        tfs = codecs.open(tmpfile, 'w', 'utf-8')
        tfs.write(content)
        tfs.close()
        print('GFW list fetched, writing...')
    except:
        print('GFW list fetch failed, use tmp instead...')
    tfs = codecs.open(tmpfile, 'r', 'utf-8')

    # Store all domains, deduplicate records
    domainList = []

    # Write list
    for line in tfs.readlines():

     if re.findall(comment_pattern, line):
         continue
     else:
         domain = re.findall(domain_pattern, line)
         if domain:
             try:
                 found = domainList.index(domain[0])
             except ValueError:
                 domainList.append(domain[0])
                 gfwListTxt.write('DOMAIN-SUFFIX,%s,Proxy,force-remote-dns\n' % (domain[0]))
         else:
             continue

    tfs.close()
    gfwListTxt.close()


def getAdList():
    # get list to block most of ads .
    # the url of  https://github.com/lhie1/Surge
    outfile = './list/adlist.txt'
    tmpfile = './list/adtmp'
    baseurl = 'https://github.com/lhie1/Surge/raw/master/Surge.conf'

    comment_pattern = '^\!|\[|^@@|\/|http|\#|\*|\?|\_|^\.|^\d+\.\d+\.\d+\.\d+'
    domain_pattern = '(\#?[\w\-\_]+\,[\/\w\.\-\_]+\,REJECT)[\/\*]*'

    fs = codecs.open(outfile, 'w', 'utf-8')
    fs.write('// thx  https://github.com/lhie1/Surge \n')
    fs.write('// updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    fs.write('\n')
    try:

        data = getList(baseurl)

        content = data.decode('utf-8')

        # write the decoded content to file then read line by line
        tfs = codecs.open(tmpfile, 'w', 'utf-8')
        tfs.write(content)
        tfs.close()
        print('adlist fetched, writing...')
    except:
        print('adlist fetch failed, use tmpfile instead...')
    # Store all domains, deduplicate records
    domainlist = []

    # Write list
    tfs = codecs.open(tmpfile, 'r', 'utf-8')
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


def genGfwConf():
    f = codecs.open('template/ss_gfwlist_conf', 'r','utf-8')
    gfwlist = codecs.open('list/gfwlist.txt', 'r','utf-8')
    adlist = codecs.open('list/adlist.txt', 'r','utf-8')
    proxy = codecs.open('ServerConfig.txt', 'r', 'utf-8-sig')
    file_content = f.read()
    adlist_buffer = adlist.read()
    gfwlist_buffer = gfwlist.read()
    proxy_buffer = proxy.read()
    gfwlist.close()
    adlist.close()
    f.close()
    proxy.close()

    file_content = file_content.replace('__ADBLOCK__', adlist_buffer)
    file_content = file_content.replace('__GFWLIST__', gfwlist_buffer)
    file_content = file_content.replace('__Proxy__', proxy_buffer)

    confs = codecs.open('configFileHere/gfwlist.conf', 'w','utf-8')
    confs.write(file_content)
    confs.close()


def genWhiteConf():
    cfs = codecs.open('template/ss_whitelist_conf', 'r','utf-8')
    gfwlist = codecs.open('list/whitelist.txt', 'r','utf-8')
    adlist = codecs.open('list/adlist.txt', 'r','utf-8')
    proxy = codecs.open('ServerConfig.txt','r','utf8')
    file_content = cfs.read()
    adlist_buffer = adlist.read()
    gfwlist_buffer = gfwlist.read()
    proxy_buffer = proxy.read()
    gfwlist.close()
    adlist.close()
    cfs.close()
    proxy.close()

    file_content = file_content.replace('__ADBLOCK__', adlist_buffer)
    file_content = file_content.replace('__GFWWHITELIST__', gfwlist_buffer)
    file_content = file_content.replace('__Proxy__', proxy_buffer)

    confs = codecs.open('configFileHere/whitelist.conf', 'w','utf-8')
    confs.write(file_content)
    confs.close()

def main():
    print('Getting GFW list...')
    getGfwList()
    print('Getting AD list...')
    getAdList()
    print('Getting white list...')
    whiteListCheck()
    print ('Generate config file: gfwlist.conf')
    genGfwConf()
    print ('Generate config file: whitelist.conf')
    genWhiteConf()
    print ('All done!')
    print('Now you need edit config file to add your server infomation.')

if __name__ == '__main__':
    main()