"""
This script performs various counts on the different files available,
like transdecoder files and annotation files.

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
from modules.functions import *

#=============================================================================#


def arguments():
    """
    set arguments
    """

    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("-a", "--an_files", dest = "an_files",
        type = isfile, required = True,
        help = "a file containing paths to all annotation files")
    parser.add_argument("-t", "--tr_files", dest = "tr_files",
        type = isfile, required = True,
        help = "a file containing paths to all transdecoder files")


    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    # get file names
    an_files = get_files_from_argument(args.an_files)
    transdecoder_files = get_files_from_argument(args.tr_files)

    # get strain ID from transdecoder filenames
    strain_ids = get_id(transdecoder_files)

    # creates transdecoder dictionary
    dtr = {}

    # creates annotation dictionary
    dan = {}

    # for each ID create a key in each dictionary
    for idts in strain_ids:
        if idts not in dtr.keys():
            dtr[idts] = {"nb_orf" : 0, "records" : []}
            dan[idts] = {}

    # fill transdecoder dictionary, create a transcript dictionary containing
    # the length of each ID, count the number of sequences for all transdecoder
    # files
    dtr, transcript, seq_count = fill_dtr(dtr, transdecoder_files)

    # create a db_count dictionary containing the number of each database by
    # annotation file
    db_count = db_by_an_file(an_files)

    # create and save db_count output
    output = "../results/db_count.txt"
    save_db_count(output, db_count)

    # create and save seq_count output
    output = "../results/seq_count.txt"
    save_seq_count(output, seq_count)

    # fill annotation dictionary
    dan = fill_dan(dan, an_files)

    # save transdecoder dictionary, annotation dictionary,
    # and transcript dictionary
    save_dtr(dtr)
    save_dan(dan)
    save_transcript(transcript)


if __name__ == '__main__':
    main()