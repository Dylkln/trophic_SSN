"""
This script combines information from three different tables, including
trophies associated with transcriptomes.

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
import csv
from modules.functions import *

#=============================================================================#


def arguments():
    """
    set arguments
    """

    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("-c", "--csv_files", dest = "csv_files",
        type = str, required = True, nargs = "+",
        help = "CSV files to merge, the first file is the one you\
        want the data happened to")
    parser.add_argument("-nf", "--name_file", dest = "name_file",
        type = isfile, required = True,
        help = "File containing all metdb ids")

    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    # save all files in a list
    files = [f for f in args.csv_files]

    # get fieldsnames for all files
    fieldnames = []
    fieldnames = determine_fieldnames(files, fieldnames)

    # initiate two lists and an index
    r_ids = []
    row_ids = []
    index = 0

    # while files exists
    while files:

        # if condition is "true", set an output filename and opens it
        if len(files) == 1:
            f_name = "MetDB_full_verified.csv"
            f_out = open(f_name, "w")

        elif index == 0:
            f_name = "metdb_with_ID.csv"
            f_out = open(f_name, "w")

        else:
            file = tempfile.NamedTemporaryFile()
            f_name = file.name
            f_out = open(f_name, "w")

        # write header of the output file
        writer = csv.DictWriter(f_out, fieldnames = fieldnames)
        writer.writeheader()

        if index == 0:

            # for each row in the first csv file
            for row in read_csv(files[0]):

                # get new row
                new_row = add_id(row, args.name_file)
                
                # if new_row is not empty, write it in the output, 
                # else, write the row in the output
                if new_row:
                    writer.writerow(new_row)
                else:
                    writer.writerow(row)        
        else:

            # determine fieldnames of the first file in files list
            fieldnames_file = []
            fieldnames_file = determine_fieldnames(files[0], fieldnames_file)
            
            # get common fielnames between first file fieldnames and all fieldnames
            common_fieldnames = set(fieldnames_file) & set(fieldnames)
            
            # if there is >= 1 fieldname(s), set the common column, 
            # else, raise an error and end the script
            if len(common_fieldnames) >= 1:
                common_column = search_for_word(common_fieldnames, "ID")
            else:
                print("ERROR : Your files have no common column names")
                break

            # if there is a common column
            if common_column:
                
                # for each row in the previous file created
                for row in read_csv(previous_file_name):
                    
                    # get new row to write it in the new file
                    new_row = get_new_row(row, common_column, files[0])
                    
                    # if new_row is not empty, write it in the output, 
                    # else, write the row in the output
                    if new_row:
                        writer.writerow(new_row)
                    else:                    
                        writer.writerow(row)
            # if there is not a common colum, raise an error and end the script
            else:
                print("ERROR : Common column not found")
                break

        # remove the first filename from the file list
        files.remove(files[0])

        index += 1

        # set the previous file name as the name of the output file
        # it just created
        previous_file_name = f_name


if __name__ == '__main__':
    main()