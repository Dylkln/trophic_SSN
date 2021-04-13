"""
This program is used to add informations to nodes from a sequence similarity
network compressed file. 

USAGE : {MANDATORY} -n [NODE_FILE] -a [ANNOTATION_FILES]

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

from modules.functions_for_table import *
import argparse

###############################################################################


def arguments():
    """
    set arguments
    """

    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("-n", "--node_file", dest = "node_file",
        type = isfile, required = True,
        help = "File containing the nodes of the sequence similarity network")
    parser.add_argument("-a", "--annotation_files", dest = "annotation_files",
        type = isfile, required = True,
        help = "File containing all annotations files")

    return parser.parse_args()


def main():
    """
    Main program function
    """
    # get arguments
    args = arguments()
    
    # get filenames
    file_names = get_files_from_argument(args.annotation_files)

    # create a compressed annotation file
    an_file = "annotation_files_all.gz"
    assemble_all_files(an_file, file_names)

    # create a compressed node file with all annotations
    node_file_full = "node_file_full.gz"
    f = gzip.open(node_file_full, "wb")
    prev_line = []
    node = 0

    for node_line in read_compressed_file(args.node_file):
        for an_line in read_compressed_file(an_file):
            
            node_list = node_line.split()
            an_list = an_line.split()

            if not prev_line:
                prev_line = node_list
                length, db, ipr = [], [], []
                node += 1

            if prev_line:
                if node == 1:
                    
                    if node_list[0] == an_list[0]:
                        length, db, ipr = add_info_to_lists(length, db, ipr, an_list)

                    if node_list[0] != an_list[0]:
                        if length:
                            write_line_to_compressed_file(length, db, ipr, node_list, f)
                            prev_line = []
                
                else:
                    i = check_prev_and_node_line(prev_line, node_list)
                    
                    if i:
                        continue

                    if not i:
                        if node_list[0] == an_list[0]:
                            length, db, ipr = add_info_to_lists(length, db, ipr, an_list)


                        if node_list[0] != an_list[0]:
                            if length:
                                write_line_to_compressed_file(length, db, ipr, node_list, f)
                                prev_line = []


if __name__ == '__main__':
    main()