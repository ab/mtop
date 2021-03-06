#!/usr/bin/python
#
# Copyright 2011 Allan Beaufour
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from optparse import OptionParser
import sys

from pymongo.connection import Connection
from pymongo.errors import AutoReconnect

from lib.runner import Runner

def main():
    parser = OptionParser(usage='mtop.py [options]\nSee also: https://github.com/beaufour/mtop')
    parser.add_option('-s', '--server',
                      dest='server', default='localhost',
                      help='connect to mongo on SERVER', metavar='SERVER')
    parser.add_option('-d', '--delay',
                      dest='delay', type=int, default=1000,
                      help='update every MS', metavar='MS')

    (options, _) = parser.parse_args()

    try:
        connection = Connection(options.server, slave_okay=True)
    except AutoReconnect, ex:
        print 'Connection to %s failed: %s' % (options.server, str(ex))
        return -1

    runner = Runner(connection, options.delay)

    rc = runner.run()

    if rc == -3:
        print 'Screen size too small'

    return rc


if __name__ == '__main__':
    sys.exit(main())
