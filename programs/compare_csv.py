"""
This program is used to compare two csv files and save common lines in a new
csv file.

USAGE : {MANDATORY} -c1 [CSV_FILE1] -c2 [CSV_FILE2]
"""

########################## MODULES TO IMPORT ##################################

from modules.__modules__ import *
import argparse
import os
import pandas as pd

###############################################################################


def isfile(path):
    """
    Check if path is an existing file
    """

    if not os.path.isfile(path):

        if os.path.isdir(path):
            err = f"{path} is a directory"
        else:
            err = f"{path} does not exist"

        raise argparse.ArgumentTypeError(err)

    return path


def arguments():
    """
    set arguments
    """

    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("-c1", "--csv_file1", dest = "csv_file1",
        type = isfile, required = True,
        help = "first csv file")
    parser.add_argument("-c2", "--csv_file2", dest = "csv_file2",
        type = isfile, required = True,
        help = "second csv file")

    return parser.parse_args()


def read_csv_file(csv1, csv2):
    """
    Reads csv files and retrieves pandas dataframes
    """
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)

    return df1, df2


def compare_dataframes(dataframe1, dataframe2, chosen_colname):
    """
    Compares two dataframes and retrieves a dataframe with common lines
    """

    return set(dataframe1[str(chosen_colname)]) & set(dataframe2[str(chosen_colname)])


def check_common_columns(df1, df2):
    """
    """

    col_names_df1 = df1.columns.tolist()
    col_names_df2 = df2.columns.tolist()

    common_colnames = set(col_names_df1) & set(col_names_df2)

    return common_colnames

def main():
    """
    Main program function
    """

    args = arguments()

    df1, df2 = read_csv_file(args.csv_file1, args.csv_file2)

    common_colnames = check_common_columns(df1, df2)

    if not common_colnames:
        raise Exception("Your CSV files have no common column names,\
please choose two CSV files with at least one common column name")
    
    if len(common_colnames) == 1:
        chosen_colname = common_colnames
        print(f"Your CSV files have one common column name,\
the program will compare datas from this column : {chosen_colname}")

    if len(common_colnames) > 1:
        print(f"Your CSV files have several common column names, please\
choose one column name from which you want the program to compare the CSV\
files, type one of the following :{list(common_colnames)}".strip())
        chosen_colname = input()
        print(f"You chose the column name {chosen_colname}")

    chosen_colname = chosen_colname
    print(chosen_colname)
    common_values = compare_dataframes(df1, df2, "NCBI ID")

    final_df_metDB = df2[df2["NCBI ID"].isin(common_values)]
    final_df_metDB = final_df_metDB.join(df1[["Mixotrophie", "Mixotypes", "Trophie"]], how ="left")
    print(final_df_metDB)
    final_df_metDB.to_csv("../results/consensus_table_data_metDB.csv", index = False, na_rep = "NA")

#    final_df_mnhn = df1[df1["NCBI ID"].isin(common_values)]
#    final_df_mnhn.to_csv("../results/consensus_table_data_mnhn.csv", index = False)

if __name__ == '__main__':
    main()