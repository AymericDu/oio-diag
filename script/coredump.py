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
import re


class CoreDump(object):

    def _replace_regex(self, regex):
        replace = {"%%": "%",
                   "%c": "\d+",
                   "%d": "\d+",
                   "%e": "[a-zA-Z-_.]+",
                   "%g": "\d+",
                   "%h": "\w+",
                   "%i": "\d+",
                   "%I": "\d+",
                   "%p": "\d+",
                   "%P": "\d+",
                   "%s": "\d+",
                   "%t": "\d+",
                   "%u": "\d+",
                   "%E": "[a-zA-Z-_.!]+",
                   }
        for k, v in replace.iteritems():
            regex = regex.replace(k, v)
        regex = ''.join(['^', regex.strip(), '$'])
        return regex

    def run(self, **kwargs):
        out = {}
        tmp = open("/proc/sys/kernel/core_pattern").read()
        # if it start by | it is processed by a software
        if '|' == tmp[0]:
            return

        regex = self._replace_regex(tmp)
        regex_index = 0
        result_list = ["/"]
        while True:
            tmp_result_list = []
            tmp_ri = regex[regex_index:].find('/')
            regex_index = tmp_ri + regex_index + 1 if tmp_ri != -1 else -1
            if regex_index != -1:
                p = re.compile(regex[:regex_index])
            else:
                p = re.compile(regex)
            for folder in result_list:
                try:
                    files = os.listdir(folder)
                except OSError:
                    if p.match(folder):
                        tmp_result_list.append(folder)
                    continue
                for elem in files:
                    if p.match('/'.join([folder, elem])):
                        separator = "/" if folder != "/" else ""
                        tmp_result_list.append(separator.join([folder, elem]))

            result_list = tmp_result_list
            if regex_index == -1:
                break

        for elem in result_list:
            out[elem.replace('/', '!')] = open(elem).read()
        return out
