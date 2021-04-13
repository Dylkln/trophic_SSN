"""
This program is used to count the number of nodes in a compressed file.

USAGE : {MANDATORY} -f [FILE] -i [ID_FILE]

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
    parser.add_argument("-f", "--file", dest = "file",
        type = isfile, required = True,
        help = "compressed file containing all nodes to count")
    parser.add_argument("-i", "--id", dest = "id",
        type = isfile, required = True,
        help = "file containing all node IDs")

    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    # get IDs
    id_dic = create_id_dict(args.id)

    # check if the node is in the node file
    for line in read_compressed_file(args.file):
        line_list = line.split()
        idt = line_list[0].replace("_", "-").lower()
        check_id(id_dic, idt)
        

    # get node count
    count = count_nodes(id_dic)

    # create node file
    node_count = "node_count.txt"

    # save nodes count in the file
    save_node_count(count, node_count)


if __name__ == '__main__':
    main()