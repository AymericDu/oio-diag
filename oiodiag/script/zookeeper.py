# Copyright (C) 2017 OpenIO SAS, as part of OpenIO SDS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ConfigParser import SafeConfigParser
from os import path
from glob import glob
from oiodiag import cmdraw, pipe, map_type


class ZooKeeper(object):

    def run(self, ns=None, **kwargs):
        def places():
            yield '/etc/oio/sds.conf'
            for f in glob('/etc/oio/sds.conf.d/*'):
                yield f
            yield path.expanduser('~/.oio/sds.conf')

        out = dict()

        c = SafeConfigParser({})
        success = c.read(places())
        if not success or not c.has_section(ns):
            return out
        conf = dict(c.items(ns))
        zookeeper = conf.get('zookeeper', None)
        if zookeeper is None:
            return out

        addr = zookeeper.rsplit(':', 1)
        host = addr[0].lstrip('[').rstrip(']')
        port = addr[1]
        mntr = pipe(['echo', 'mntr'])
        for line in cmdraw(['nc', host, port], stdin=mntr.stdout):
            k, v = line.split("\t")
            out[k.strip()] = map_type(v.strip())
        return out
