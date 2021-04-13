"""
This program is used to count the number of transcript by ID.

USAGE : {MANDATORY} -f [FILES]

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
        help = "a list of files")

    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    # get file_names list
    files = get_files_from_argument(args.files[0])
    transcript_files = get_files_from_argument(args.files[1])

    # get IDs
    idts = get_strain_id(files)

    # create a dictionary with the number of transcript by ID
    count_dict = count_transcript(idts, transcript_files)

    # define the name of the file to save the dictionary
    transcript_count_file = "trancript_count.txt"

    # save the dictionary
    save_data_from_dict_in_file(count_dict, transcript_count_file)


if __name__ == '__main__':
    main()