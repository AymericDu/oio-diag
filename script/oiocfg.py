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

import os
from oio.diag import FileSet


def _walk(paths):
    for path in paths:
        for base, dirs, files in os.walk(path):
            for f in files:
                yield '/'.join((base, f))


class EtcFiles(object):

    def run(self, **kwargs):
        allpaths = ('/etc/oio/sds',
                    '/etc/oio/sds.conf',
                    '/etc/oio/sds.conf.d')
        return FileSet(_walk(allpaths))
