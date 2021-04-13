"""
This program is used to find path with a similar pattern.

USAGE : {MANDATORY} -p [PATTERN] -d [ABSOLUTE_PATH_TO_DIRECTORY]

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

from modules.functions import *
import argparse

###############################################################################


def arguments():
    """
    set arguments
    """

    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("-p", "--pattern", dest = "pattern",
        type = str, required = True,
        help = "the pattern of the files to be found")
    parser.add_argument("-d", "--path", dest = "path",
        type = str, required = True,
        help = "absolute path to directory")

    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    # get all matches in a list
    result = find_file(args.pattern, args.path)
    
    # name the output file
    file = "../results/files_found.txt"

    # save in output file
    save_to_txt(result, file)


if __name__ == '__main__':
    main()