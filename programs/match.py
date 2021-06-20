"""
This script extracts the METdb part of a bigger sequence similarity network.

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


#================================== Modules ==================================#

import argparse
import gzip
from modules.functions import *

#=============================================================================#


def arguments():
    """
    set arguments
    """

    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("-f", "--file", dest = "file",
        type = str, required = True,
        help = "a file containing paths to all annotation files")
    parser.add_argument("-p", "--pattern", dest = "pattern",
        type = str, required = True,
        help = "a file containing paths to all transdecoder files")
    parser.add_argument("-o", "--output", dest = "output",
        type = str, required = True,
        help = "a file containing paths to all transdecoder files")

    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    # open the output file in write mode
    f_out = gzip.open(args.output, "w")

    # determine the header for the output file
    header = "queryId:frame\tqueryLength\tqueryFrom\tqueryTo\ttargetId:frame\ttargetLength\ttargetFrom\ttargetTo\tmatchLength\tpercentIdentity\tpercentPositivity\tscore\teValue\tbitscore\n"

    # write headers in binary
    f_out.write(header.encode())

    # for line in a compressed file
    for line in read_compressed_file(args.file):

        # retrives the number of times a pattern is found in the line
        p = len(re.findall(args.pattern, line))

        if p == 2:

            # write the line in the output file
            f_out.write(line.encode())


if __name__ == '__main__':
	main()