#!/usr/bin/python
# 
#  Copyright (C) 2011 Raghu Udiyar <raghusiddarth@gmail.com>
#  
#  This copyrighted material is made available to anyone wishing to use,
#  modify, copy, or redistribute it subject to the terms and conditions
#  of the GNU General Public License, either version 2 of the License, or
#  (at your option) any later version
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 
# 
#  Description:
#  Used to pupulate data.db with documentation for /proc tunables
# 
#  Author: Raghu Udiyar <raghusiddarth@gmail.com>
#

import sys
import re
import shelve
import argparse
import subprocess

from procinfo.tunable import Tunable

KERNEL = subprocess.Popen(['rpm', '-q', 'kernel-doc'],
                         stdout=subprocess.PIPE).communicate()[0]
try:
    KERNELVER = KERNEL.split('-')[2]
except:
    print "[Error] Could not determine kernel doc version"
    sys.exit(1)

KERNELDOC = '/usr/share/doc/kernel-doc-%s/Documentation' % KERNELVER
sysctl_doc = '%s/sysctl/' % KERNELDOC
TXTFILES = ('vm.txt', 'kernel.txt', 'fs.txt', 'net.core.txt', 'sunrpc.txt')
#TXTFILES = ('net.core.txt',)

DBPATH = "data.db"
DATAPATH= "data/docs/"
KEYDB = "keys.db"

def process_frame(frame, sysctl):

    p = re.compile(r'\n\n([a-zA-Z0-9 &_()*,:-]+)[:]*\n[-]*\n')
    l = p.split(frame, maxsplit=1)

    q = re.compile(r'[,&: ]*')
    tlist = q.split(l[1])

    tlist = filter(None, tlist)                   # remove empty elements from list
    tlist = filter(lambda x: "(" not in x, tlist) # remove () from the list
    tlist = filter(lambda x: ")" not in x, tlist) 

    for sys in tlist:
        sys = sys.strip()       # remove whitespace
        t = Tunable(sysctl + '.' + sys, "n/a", l[2])
        write_obj(t)
        print "Written : '%s'" % t.sysctl
    return


def parse_file(fname, sysctl):

    data = fname.read()
    p = re.compile(r"={3,}")
    data_list = p.split(data)
    frame_list = data_list[2:]  # discard first 2 elements
    for frame in frame_list:
        process_frame(frame, sysctl)

    return


def get_sysctl_info():

    for file_name in TXTFILES:
        file_path = DATAPATH + file_name
        print file_path

        try:
            fname = open(file_path, 'r')
        except:
            print "[Error] Can't open data file(s)"
            sys.exit(0)

        sysctl = file_name.split('.txt')[0]
        parse_file(fname, sysctl)   
        fname.close()
    
    write_keys(open(KEYDB, "w")) # Finaly write keydb
    print "keydb written"
    return

def get_data(source='terminal'):
    
    if source == 'terminal':
        sysctl = raw_input("sysctl? ")
        default = raw_input("default? ")
        desc = raw_input("describe? ")
        t = Tunable(sysctl, default, desc)
        return t

def write_keys(out=sys.stdout):
    db = shelve.open(DBPATH)
    try:
        klist = db.keys()
    except:
        print "[Error] Can't open key db"
        sys.exit(1)
    finally:
        db.close()
    for sysctl in klist:
        out.write(sysctl+"\n")


def write_obj(t):

    db = shelve.open(DBPATH)
    try:
        db[t.sysctl] = t
    finally:
        db.close()

def get_obj():

    sysctl = raw_input("sysctl? ")
    db = shelve.open(DBPATH)
    try:
        t = db[sysctl]
    except KeyError:
        print "[Error] Invalid Key"
        db.close()
        sys.exit(1)
    
    db.close()
    t.display()
    

def getargs():
        parser = argparse.ArgumentParser(description='Information on /proc tunables.')

        parser.add_argument('--writedb', action='store_true')
        parser.add_argument('--list', action='store_true')
        parser.add_argument('commands', metavar='commands', nargs='?', type=str, help =
                            'write/read', choices=['write', 'read'])
        parser.add_argument('--kernel', action='version', version=KERNELVER,
                            help= 'Show kernel version')
        args = parser.parse_args()

        if args.writedb:
            get_sysctl_info()

        if args.list:
            write_keys(sys.stdout)
        
        if args.commands  == 'write':
            t = get_data(source='terminal')
            write_obj(t)
        elif args.commands == 'read':
            get_obj()


def main():
    getargs()


if __name__ == '__main__':
    main()
    sys.exit(0)


# vim: ts=4 sw=4 et
