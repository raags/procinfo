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
#  Author: Raghu Udiyar <raghusiddarth@gmail.com>
#

import sys

class Tunable:
    """ This represents a proc tunable entry """

    def __init__(self, sysctl, default, desc):
        self.sysctl = sysctl
        self.default = default
        self.desc = desc

    def display(self):
        print self.sysctl
        print ""
        print self.desc

if __name__ == '__main__':
    print Tunable.__doc__
    sys.exit(0)

# vim: ts=4 sw=4 et
