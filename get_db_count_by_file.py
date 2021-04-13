"""
This program is used to count the number of database by annotation files.

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
        help = "compressed file containing all nodes to count")

    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments    
    args = arguments()

    # get filenames
    files = get_files_from_argument(args.file)

    # create database count dictionary
    db_count = get_db_count_by_file(files)

    # create database count file
    db_count_file = "db_count_by_annotation_file.txt"

    # save the dictionary into the file
    save_db_count_by_file(db_count_file, db_count)


if __name__ == '__main__':
    main()