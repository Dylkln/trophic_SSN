"""
This program is used to merge two files with at least one column name in common.

USAGE : {MANDATORY} -f1 [FILE_1] -f2 [FILE_2] -cn [COLUMN_NAME]

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
    parser.add_argument("-f1", "--file_1", dest = "file_1",
        type = isfile, required = True,
        help = "a first file containing data to be merged with the second one")
    parser.add_argument("-f2", "--file_2", dest = "file_2",
        type = isfile, required = True,
        help = "a second file containing data to be merged with the first one")
    parser.add_argument("-cn", "--column_name", dest = "column_name",
        type = str, required = True,
        help = "the name of the column used as the basis of the merge")


    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()
    
    # Create pandas dataframes from csv file
    df1, df2 = read_table_file(args.file_1, args.file_2)

    # Merge both dataframe into one final dataframe
    final_df = pd.merge(df1, df2, on = args.column_name, how = "outer")
   
    # define the path to the file to be saved
    final_file = "merged_file.csv"

    # save the dataframe in a csv file
    final_df.to_csv(final_file, index = False, na_rep = "NA")


if __name__ == '__main__':
    main()