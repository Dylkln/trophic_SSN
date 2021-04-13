"""
This program is used to count the number of sequences in files.

USAGE : {MANDATORY} -f [FILE]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
A copy of the GNU General Public License is available at
http://www.gnu.org/licenses/gpl-3.0.html
"""

__author__ = "KLEIN Dylan"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "klein.dylan@outlook.com"


########################## MODULES TO IMPORT ##################################

import argparse
from modules.functions_for_table import *

###############################################################################


def arguments():
    """
    set arguments
    """

    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("-f", "--file", dest = "file",
        type = isfile, required = True,
        help = "file containing a list of files with the sequences to count")

    return parser.parse_args()

 
def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    # get a list of files
    files = get_files_from_argument(args.file)

    # get the number of sequences contained in the files
    seq_count, record = count_seq_in_files(files)

    # a file to save de seq count
    file_seq_count = "seq_count.txt"
    file_record = "seq_ids.txt"

    # save the seq count in the file
    save_seq_count(file_seq_count, seq_count)
    save_record(file_record, record)

if __name__ == '__main__':
    main()