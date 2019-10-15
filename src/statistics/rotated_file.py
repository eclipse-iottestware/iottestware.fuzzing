# ********************************************************************************
# Copyright (c) 2019 Alexander Kaiser
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0.
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors:
#   Alexander Kaiser - initial API and implementation
# ********************************************************************************

import os
import re


def get_rotated_files(base_file_path):
    """
    Workaround for the described idea below
    from a given base file, this function returns a list of all rotated files
    :param base_file_path:
    :return:
    """
    base_dir = os.path.dirname(base_file_path)

    # get the base file name
    file_name = os.path.basename(base_file_path)

    # remove rotation index if given already in filename
    r_rot_idx = r'\S+\.log\.[0-9]+'
    if re.match(r_rot_idx, file_name):
        # filename contains rotation idx at the end e.g. file.log.1
        tokens = file_name.split('.')   # split into ['file', 'log', '1']
        file_name = '.'.join(tokens[:2])

    r_rotation_files = r'{}\.[0-9]+'.format(file_name)
    files = list()
    # search for rotated files based on file_name
    for f in os.listdir(base_dir):
        if re.match(r_rotation_files, f):   # filter only rotation files for file_name
            files.append(f)

    # files append can be unsorted
    files.sort(key=lambda f: int(f.split('.')[2]))  # sort by index
    files.insert(0, file_name)  # set the base file as the first one

    # now prefix each filename with base dir
    for i, f in enumerate(files):
        files[i] = os.path.join(base_dir, f)

    return files


"""
TODO: wrapper for rotated files which allows to read multiple consecutive files as if it was a single file
e.g. file.log.1, file.log.2, file.log.2... exist

with open('file.log') as f:
    for l in f:
        print(l)

would print all lines starting first line from file.log and ending with last line from file.log.N
"""

"""
class RotatedFileWrapper:

    def __init__(self, file_path):
        self._file_path = file_path
        self._current_file = None

    def __enter__(self):
        self._current_file = open(self._file_path, 'r')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._current_file.close()
"""
