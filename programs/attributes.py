"""
This script creates an "attributes" file in order to add the attributes of the
different nodes to the sequence similarity network.

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
    parser.add_argument("-s", "--seq_file", dest = "seq_file",
        type = isfile, required = True,
        help = "File containing all the ORFs")
    parser.add_argument("-a", "--annotation_files", dest = "annotation_files",
        type = isfile, required = True,
        help = "File containing all annotations filenames")
    parser.add_argument("-t", "--table_file", dest = "table_file",
        type = isfile, required = True,
        help = "CSV file containing taxonomic and trophic information")

    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    # get filenames
    file_names = get_files_from_argument(args.annotation_files)

    # get annotation file to open and the ID linked to the seq_file
    an_file, name = get_an_file(args.seq_file, file_names)

    # get fieldnames
    k = ["peptides", "Phylum_Metdb", "Class_Metdb", "Order_Metdb", 
    "Family_Metdb", "Genus_Metdb", "Species_Metdb", "Trophy","length",
    "identifiant", "interproscan"]

    # set a path to a directory
    p = "../results/attributes"

    # if path to directory does not exist it creates the path
    if not os.path.exists(p):
        os.mkdir(p)

    # name the output file and open it
    output = f"{p}/{name}_attributes.txt"
    f = open(output, "w")

    # write header to the output file
    writer = csv.DictWriter(f, fieldnames = k)
    writer.writeheader()

    # create a dictionary containing taxonomy and trophic information
    seq_dict = add_keys_to_seq_dict(k, name, args.table_file)

    # deepcopy the dictionary in order to reset it after each sequence ID
    reset_dict = copy.deepcopy(seq_dict)

    # for each sequence ID in file
    for seq in read_file(args.seq_file):

        # fill the dictionary with the annotation linked to the sequence ID
        seq_dict = fill_seq_dict(seq_dict, an_file, seq)

        # write the attribute in the file
        writer.writerow(seq_dict)

        # reset the seq_dict
        seq_dict = copy.deepcopy(reset_dict)


if __name__ == '__main__':
    main()