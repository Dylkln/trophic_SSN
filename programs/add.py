"""
This script adds vertices attributes.

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
    parser.add_argument("-v", "--vertices_file", dest = "vertices_file",
        type = isfile, required = True,
        help = "The file containing all nodes")
    parser.add_argument("-o", "--output", dest = "output",
        type = str, required = True,
        help = "the output file with repeating nodes removed")
    parser.add_argument("-a", "--attribute_files", dest = "attribute_files",
        type = str, required = False, default = None,
        help = "all files containing the attributes")


    return parser.parse_args()

def main():


    args = arguments()

    fieldnames = ["name", "prefix", "Phylum_Metdb", "Class_Metdb",
    "Order_Metdb", "Family_Metdb", "Genus_Metdb", "Species_Metdb",
    "Trophy", "length", "identifiant", "interproscan"]
    
    files = get_files_from_argument(args.attribute_files)

    f_out = open(args.output, "w")
    
    writer = csv.DictWriter(f_out, delimiter = ";", fieldnames = fieldnames)
    writer.writeheader()

    name_set = set([])
    
    for row in read_csv(args.vertices_file):
        if row["name"] not in name_set:
            name_set.add(row["name"])
    
    ns = sorted(name_set)
    i = len(ns)

    for index, n in enumerate(ns):


        if index == 0:

            nset = set([n])
            previous_n = "-".join(n.split("-")[0:2])

        
        elif index + 1 <= i:


            if previous_n == "-".join(n.split("-")[0:2]):

                nset.add(n)


            else:

                nset = sorted(nset)
                fn = get_fname(nset[0], files)

                if fn:

                    rows = get_rows(nset, fn)
                    write_rows(writer, rows)
                    nset = set([n])
                    previous_n = "-".join(n.split("-")[0:2])

                else:
                    nset = set([n])
                    previous_n = "-".join(n.split("-")[0:2])

        
        elif index + 1 >= i:


            if previous_n == "-".join(n.split("-")[0:2]):

                nset.add(n)
                nset = sorted(nset)
                fn = get_fname(nset[0], files)

                if fn:
                    rows = get_rows(nset, fn)
                    write_rows(writer, rows)


            else:

                nset = set([n])
                fn = get_fname(nset[0], files)

                if fn:
                    rows = get_rows(nset, fn)
                    write_rows(writer, rows)


if __name__ == '__main__':
    main()
