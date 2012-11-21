#!/usr/bin/env python

import subprocess, sys, re


DEFAULT_FKEY = 7 # by default all Fx is F7 during execution of xlock
DEFAULT_ENCODE = 'utf8' # by default encoding of xmap is utf

fkey_regex = re.compile(r'^(.+=\sF\d+\s.+)$', re.M)


def scan_fkeys():
    map = subprocess.getoutput(r'xmodmap -pke')
    aro = [i.split() for i in fkey_regex.findall(map)]

    return map, aro


def switch_xmodmap(aro, encoding):
    p = subprocess.Popen(['xmodmap', '-'], stdin=subprocess.PIPE)
    p.communicate(input='\n'.join([' '.join(i) for i in aro]).encode(encoding))


def xlock(args):
    xlock = subprocess.Popen(['xlock'] + args)
    xlock.communicate()


if __name__ == '__main__':
    map = scan_fkeys()[1]
    switch_xmodmap([i[:2] + map[DEFAULT_FKEY-1][2:] for i in map], DEFAULT_ENCODE)
    xlock(sys.argv[1:])
    switch_xmodmap(map, DEFAULT_ENCODE)
