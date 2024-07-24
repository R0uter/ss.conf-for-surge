import codecs
from shutil import copyfile
import os, sys


def txt2list(src, dst, removed_str):
    print('Generate surge rule-set ' + dst)
    fp = open(dst, 'w')
    lines = open(src).readlines()  #打开文件，读入每一行
    for s in lines:
        fp.write(s.replace(removed_str, ''))
    fp.close()
    print(dst + ' ' + 'done')


txt2list('list/adlist.txt', 'list/adlist.list', ',REJECT')
txt2list('list/whitelist.txt', 'list/whitelist.list', ',DIRECT')
txt2list('list/gfwlist.txt', 'list/gfwlist.list', ',Proxy,force-remote-dns')

print('Generate surge rule-set complele')
