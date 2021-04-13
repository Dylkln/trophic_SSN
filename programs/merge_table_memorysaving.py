"""
This program is used to merge two files with at least one column name in common.

USAGE : {MANDATORY} -f [FILES] -cn [COLUMN_NAME] -d [DELIMITER]

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
    parser.add_argument("-f", "--files", dest = "files",
        type = str, required = True, nargs = "+",
        help = "a list of files to merge")
    parser.add_argument("-cn", "--column_name", dest = "column_name",
        type = str, required = True,
        help = "the column name to merge on")
    parser.add_argument("-d", "--delimiter", dest = "delimiter",
        type = str, required = True,
        help = "the delimiter used in the file")

    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    # get delimiters
    delimiter = get_delimiters(args.delimiter)

    # save all fieldnames of all csv passed in argument
    fieldnames = determine_fieldnames(args.files, delimiter)

    # save data from csv files, remove redundancies and merge data
    csv_data = copy_data(args.files, fieldnames, args.column_name, delimiter)
    
    # define the path to the file to be saved
    final_file = "merged_file.csv"

    # create a new csv file with the merges values
    write_csv(final_file, fieldnames, csv_data)


if __name__ == '__main__':
    main()