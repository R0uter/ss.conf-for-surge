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
import os


def get_list(list_url):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',  # Force certificate check.
        ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )

    data = http.request('GET', list_url, timeout=10).data
    return data


def white_list_check():
    dnsmasq_china_list = 'https://r0uter.github.io/gfw_domain_whitelist/whitelist.pac'
    try:

        content = get_list(dnsmasq_china_list)
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
        
        domain = re.findall(r'(?<=")[a-z0-9|\-]+\.\w+', line)
        if len(domain) > 0:
            whitelistTxt.write('DOMAIN-SUFFIX,%s,DIRECT\n'%(domain[0]))

    whitelist.close()
    whitelistTxt.close()


def get_gfw_list():
    # the url of gfwlist
    base_url = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'

    comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    tmp_file = './list/tmp'
    gfwListTxt = codecs.open('./list/gfwlist.txt', 'w+', 'utf-8')
    gfwListTxt.write('// SS config file for surge with gfw list \n')
    gfwListTxt.write('// updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    gfwListTxt.write('\n')

    try:

        data = get_list(base_url)
        content = codecs.decode(data, 'base64_codec').decode('utf-8')
        # write the decoded content to file then read line by line
        tfs = codecs.open(tmp_file, 'w', 'utf-8')
        tfs.write(content)
        tfs.close()
        print('GFW list fetched, writing...')
    except:
        print('GFW list fetch failed, use tmp instead...')
    tfs = codecs.open(tmp_file, 'r', 'utf-8')

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


def get_ad_list():
    # get list to block most of ads .
    # the url of  https://github.com/lhie1/Surge
    outfile = './list/adlist.txt'
    tmpfile = './list/adtmp'
    baseurl = 'https://github.com/lhie1/Rules/raw/master/Quantumult/Quantumult.conf'

    comment_pattern = '^\!|\[|^@@|\/|http|\#|\*|\?|\_|^\.|^\d+\.\d+\.\d+\.\d+'
    domain_pattern = '(\#?[\w\-\_]+\,[\/\w\.\-\_]+\,REJECT)[\/\*]*'

    fs = codecs.open(outfile, 'w', 'utf-8')
    fs.write('// thx  https://github.com/lhie1/Surge \n')
    fs.write('// updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    fs.write('\n')
    try:

        data = get_list(baseurl)
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


def gen_gfw_conf():
    f = codecs.open('template/ss_gfwlist_conf', 'r','utf-8')
    gfw_list = codecs.open('list/gfwlist.txt', 'r','utf-8')
    ad_list = codecs.open('list/adlist.txt', 'r','utf-8')
    proxy = codecs.open('ServerConfig.txt', 'r', 'utf-8-sig')
    file_content = f.read()
    ad_list_buffer = ad_list.read()
    gfw_list_buffer = gfw_list.read()
    proxy_buffer = proxy.read()
    gfw_list.close()
    ad_list.close()
    f.close()
    proxy.close()

    file_content = file_content.replace('__ADBLOCK__', ad_list_buffer)
    file_content = file_content.replace('__GFWLIST__', gfw_list_buffer)
    file_content = file_content.replace('__Proxy__', proxy_buffer)

    confs = codecs.open('configFileHere/gfwlist.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()


def gen_white_conf():
    cfs = codecs.open('template/ss_whitelist_conf', 'r', 'utf-8')
    gfw_list = codecs.open('list/whitelist.txt', 'r', 'utf-8')
    ad_list = codecs.open('list/adlist.txt', 'r', 'utf-8')
    proxy = codecs.open('ServerConfig.txt', 'r', 'utf8')
    file_content = cfs.read()
    ad_list_buffer = ad_list.read()
    gfw_list_buffer = gfw_list.read()
    proxy_buffer = proxy.read()
    gfw_list.close()
    ad_list.close()
    cfs.close()
    proxy.close()

    file_content = file_content.replace('__ADBLOCK__', ad_list_buffer)
    file_content = file_content.replace('__GFWWHITELIST__', gfw_list_buffer)
    file_content = file_content.replace('__Proxy__', proxy_buffer)

    confs = codecs.open('configFileHere/whitelist.conf', 'w','utf-8')
    confs.write(file_content)
    confs.close()


def gen_geo_ip_white_conf():
    cfs = codecs.open('template/ss_geoip_white_conf', 'r', 'utf-8')
    ad_list = codecs.open('list/adlist.txt', 'r', 'utf-8')
    proxy = codecs.open('ServerConfig.txt', 'r', 'utf8')
    file_content = cfs.read()
    ad_list_buffer = ad_list.read()
    proxy_buffer = proxy.read()
    ad_list.close()
    cfs.close()
    proxy.close()

    file_content = file_content.replace('__ADBLOCK__', ad_list_buffer)
    file_content = file_content.replace('__Proxy__', proxy_buffer)

    confs = codecs.open('configFileHere/geoip_whitelist.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()


def gen_cn_conf():
    cfs = codecs.open('template/ss_cn_conf', 'r', 'utf-8')
    ad_list = codecs.open('list/adlist.txt', 'r', 'utf-8')
    proxy = codecs.open('ServerConfig.txt', 'r', 'utf8')
    file_content = cfs.read()
    ad_list_buffer = ad_list.read()
    proxy_buffer = proxy.read()
    ad_list.close()
    cfs.close()
    proxy.close()

    file_content = file_content.replace('__ADBLOCK__', ad_list_buffer)
    file_content = file_content.replace('__Proxy__', proxy_buffer)

    confs = codecs.open('configFileHere/cn.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()


def main():
    os.makedirs(os.path.dirname('./list/'), exist_ok=True)
    os.makedirs(os.path.dirname('./configFileHere/'), exist_ok=True)
    print('Getting GFW list...')
    get_gfw_list()
    print('Getting AD list...')
    get_ad_list()
    print('Getting white list...')
    white_list_check()
    print('Generate config file: gfwlist.conf')
    gen_gfw_conf()
    print('Generate config file: whitelist.conf')
    gen_white_conf()
    print('Generate config file: geoip_whitelist.conf')
    gen_geo_ip_white_conf()
    print('Generate back to china config file: cn.conf')
    gen_cn_conf()
    print('All done!')
    print('Now you need edit config file to add your server infomation.')


if __name__ == '__main__':
    main()
