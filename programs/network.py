"""
This script creates a sequence similarity network and is used to study it.

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
    parser.add_argument("-e", "--edges_file", dest = "edges_file",
        type = isfile, required = True, nargs = "+",
        help = "")
    parser.add_argument("-v", "--vertices_file", dest = "vertices_file",
        type = isfile, required = True, nargs = "+",
        help = "")

    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()
    
    # get number of files
    l_e = len(args.edges_file)

    # initialize the index
    i = 0

    while i < l_e:

        # get coverage percentage
        cov = args.edges_file[i].split("_")[2]
        
        # get identity percentage
        ident = args.edges_file[i].split("_")[3].split(".")[0]

        # creates pandas dataframe of edges and nodes
        edges = pd.read_csv(args.edges_file[i], sep = ";")
        nodes = pd.read_csv(args.vertices_file[i], sep = ";")

        # create an igraph Graph
        g = ig.Graph.DataFrame(edges, directed = False, vertices = nodes)
        
        # remove isolated nodes
        to_del = [v.index for v in g.vs if v.degree() == 0]
        g.delete_vertices(to_del)

        # decompose graph into subgraph with minimum 3 neighbours
        g_cc = g.decompose(minelements = 3)

        # get number of connected components
        nb_of_subgraph = len(g_cc)

        # get function, phylum, genus and trophy dictionaries
        fn, tp, tg, tr, ab, db_sp = get_data_from_cc(g_cc)
    
        # get percentages of function, phylum, genus and trophy dictionaries
        fn_p, tp_p, tg_p, tr_p = get_data_percent(fn, tp, tg, tr)


        # get trophy count, unique trophy, homogeneity and entropy
        tr_c, u_tr, hi, f_en = get_data_from_cc_dicts(tr, db_sp, fn_p)

        # get the number of IDs contained in each connected component
        cl = get_cc_len(fn)

        # get abudance distribution
        ab_d = get_abund_distrib(ab)

        
        # check path
        p = f"../results/{cov}_{ident}"

        if not os.path.exists(p):
            os.mkdir(p)

        # save all values extracted from the graph
        output = f"../results/{cov}_{ident}/abund_matrix_{cov}_{ident}.tsv"
        save_dict_of_dict(ab, output)

        output = f"../results/{cov}_{ident}/abund_matrix_distrib_{cov}_{ident}.tsv"
        save_dict(ab_d, output)

        output = f"../results/{cov}_{ident}/function_percentage_{cov}_{ident}.tsv"
        save_dict_of_dict(fn_p, output)
    
        output = f"../results/{cov}_{ident}/phylum_percentage_{cov}_{ident}.tsv"
        save_dict_of_dict(tp_p, output)

        output = f"../results/{cov}_{ident}/genus_percentage_{cov}_{ident}.tsv"
        save_dict_of_dict(tg_p, output)

        output = f"../results/{cov}_{ident}/trophy_percentage_{cov}_{ident}.tsv"
        save_dict_of_dict(tr_p, output)

        output = f"../results/{cov}_{ident}/cc_nb_{cov}_{ident}.txt"
        save_dict(cl, output)

        output = f"../results/{cov}_{ident}/trophy_count_{cov}_{ident}.tsv"
        save_dict_of_dict(tr_c, output)

        output = f"../results/{cov}_{ident}/unique_trophy_{cov}_{ident}.tsv"
        save_dict(u_tr, output)

        output = f"../results/{cov}_{ident}/homogeneity_index_{cov}_{ident}.tsv"
        save_dict_of_dict(hi, output)

        output = f"../results/{cov}_{ident}/entropy_by_function_{cov}_{ident}.tsv"
        save_dict(f_en, output)

        # save the graph into a graphml format
        g.write(f = f"../results/{cov}_{ident}/graph_ssn_{cov}_{ident}", format = "graphml")

        # increment the index to go on the next files
        i += 1


if __name__ == '__main__':
    main()