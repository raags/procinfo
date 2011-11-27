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
#   Get document information for /proc tunables 
# 
#  Author: Raghu Udiyar <raghusiddarth@gmail.com>
#
# Example of usage:
# 
# $ procinfo -h
#

import os
import sys
import argparse
import shelve
import fnmatch
#from tunable import Tunable

VERSION = '0.01'

_ROOT  = os.path.abspath(os.path.dirname(__file__))
_DB    = "data.db"
_KEYDB = "keys.db"

DBPATH = os.path.join(_ROOT, 'data', _DB)
KEYDB  = os.path.join(_ROOT, 'data', _KEYDB)


def parse_query(raw_query):
    """ Convert to 'dot' form """
    
    query = raw_query.replace('/','.').replace('.proc.sys.','')
    return query

def search(raw_query):
        try:
            fname = open(KEYDB, 'ro')
        except:
            print "[Error] Could not open key db"
            sys.exit(1)
        query = parse_query(raw_query)
        lkey = []
        ldata = fname.read().split('\n')[:-1]
        for key in ldata:
            if fnmatch.fnmatch(key, query):
                lkey.append(key)

        if len(lkey) == 1:
            get_key(lkey[0])
        else: 
            if len(lkey) > 1:
                 for key in lkey:
                      print key
            else:
                print "Not found!"

def list_keys():
    try:
        db = shelve.open(DBPATH)
    except:
        print "[Error] Could not open key db"
        sys.exit(1)

    klist = db.keys()
    db.close()

    for sysctl in klist:
        print sysctl

def get_key(query):
    db = shelve.open(DBPATH)
    try:
        t = db[query]
    except KeyError:
        print "[Error] Key not found"
        sys.exit(1)
    finally:
        db.close()
    t.display()


def getargs():
    parser = argparse.ArgumentParser(description='Information on /proc or sysctl\
                                     tunables')
    parser.add_argument('--list', action='store_true', help=
                       'List all available entries')
    parser.add_argument('query', metavar="query", nargs='?', type=str, help= 
                        'Query sysctl key or /proc entry \n eg: vm.swappiness or /proc/vm/swappiness')
    parser.add_argument('--version', action='version', version=VERSION)

    args = parser.parse_args()

    if args.list:
        list_keys()

    if args.query:
        q = args.query
        search(q)

def main():
    getargs()

if __name__ == '__main__':
    main()
    exit(0)


# vim: ts=4 sw=4 et
