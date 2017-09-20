#!/usr/bin/env python
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

import argparse
import os
import pkg_resources
import shutil
import tarfile

output_list = ['file', 'tar']


def load_modules(group_name):
    modules = []
    for entry_point in pkg_resources.iter_entry_points(group_name):
        modules.append(entry_point.load(require=False))
    return modules


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars
    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


def build_arg_parser():
    log_parser = argparse.ArgumentParser(add_help=False)
    parser = argparse.ArgumentParser(parents=[log_parser])
    parser.add_argument(
            '--oio-ns',
            dest='ns',
            default=env('OIO_NS'),
            help='Namespace name (Env: OIO_NS)',
    )

    parser.add_argument(
            '--gridinit-sock',
            dest='gridinit_sock',
            help='the fullpath of the gridinit socket',
    )

    parser.add_argument(
            '--output',
            dest='output',
            default=output_list[0],
            choices=output_list,
            help='select the ouput to chose'
    )
    return parser


class OutputManager(object):

    def __init__(self):
        self.directory = 'result_test'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def create_output(self, module, result):
        if isinstance(result, dict):
            for k, v in result.iteritems():
                with open('%s/%s.%s' % (self.directory,
                                        module, k), 'w') as output_file:
                    output_file.write(v)
            return
        if isinstance(result, list):
            for i, v in enumerate(result):
                with open('%s/%s.%d' % (self.directory,
                                        module, i), 'w') as output_file:
                    output_file.write(v)
        else:
            with open('%s/%s' % (self.directory,
                                 module), 'w') as output_file:
                output_file.write(result)

    def finalize(self):
        pass


class ArchiveOutputManager(OutputManager):

    def finalize(self):
        with tarfile.open('%s.tar' % self.directory, 'w') as tar:
            tar.add(self.directory)
        shutil.rmtree(self.directory)


class MailOutputManager(ArchiveOutputManager):

    def finalize(self):
        super(MailOutputManager, self).finalize()


def make_output_manager(name):
    if name == 'file':
        return OutputManager()
    if name == 'tar':
        return ArchiveOutputManager()


def main():
    args = build_arg_parser().parse_args()
    kwargs = {}
    if args.ns is not None:
        kwargs['ns'] = args.ns
    if args.gridinit_sock is not None:
        kwargs['gridinit_sock'] = args.gridinit_sock

    outputManager = make_output_manager(args.output)
    tools_modules = load_modules("oio.tools")
    for tool in tools_modules:
        result = tool().run(**kwargs)
        outputManager.create_output(tool.__name__, result)

    outputManager.finalize()


if __name__ == '__main__':
    main()
