import numpy as np
import pandas as pd
import ast
import networkx as nx
from scipy.stats import zscore


# This code performs an analysis of hypergraphs constructed from high-order interdependencies (HOI) data,
# focusing on computing various centrality measures and comparing them to a random baseline. 
# The process starts by loading average HOI values from both empirical and randomized datasets. 
# It then constructs hypergraphs by selecting a subset of triplets, either based on their redundancy or synergy. 
# Centrality measures—specifically, eigenvector centrality, betweenness centrality, and degree centrality—are computed for these hypergraphs. 
# The code further runs a parallelized process to generate and compute these centralities across multiple randomized hypergraphs,
# aggregates the results, and determines significance thresholds for each centrality measure. 
# Finally, the results are saved and the significance thresholds are printed, 
# providing insight into the network structure and its deviation from randomness

#Openining the two files witht the average HOI values
path='Average_Data/average_triplets.csv'
path_random='Average_Data/average_triplets_random.csv'
#path_LR='Average_Data/LR_average_df.csv'
#path_RL='Average_Data/RL_average_df.csv'

mean_HOI=pd.read_csv(path,index_col=0)
mean_HOI_random=pd.read_csv(path_random,index_col=0)
#mean_HOI_RL=pd.read_csv(path_RL,index_col=0)

import numpy as np
import pandas as pd
import ast
import random

fraction=0.005
max_workers=10

def create_hypergraph(dataframe, sort_column='Mut Info_normalized', mode='redundancy', random_selection=False):
    # If random selection is enabled, select all triplets randomly
    if random_selection:
        shuffled_df = dataframe.sample(frac=1).reset_index(drop=True)
    else:
        # Sort the DataFrame based on the mode
        if mode == 'redundancy':
            shuffled_df = dataframe.sort_values(sort_column, ascending=False).copy()
        elif mode == 'synergy':
            shuffled_df = dataframe.sort_values(sort_column, ascending=True).copy()
        else:
            raise ValueError("Mode must be either 'redundancy' or 'synergy'")

    # Calculate the number of rows for the top 1% (you can adjust this percentage as needed)
    num_rows = int(len(shuffled_df) * fraction)

    # Select the top percentage of the DataFrame
    top_df = shuffled_df.head(num_rows).copy()

    # Parse the 'nplets' column
    top_df['nplets'] = top_df['nplets'].apply(ast.literal_eval)

    # Number of triplets
    n = len(top_df['nplets'])

    # Initialize the adjacency matrix
    H = np.zeros((n, n), dtype=int)

    # Populate the adjacency matrix
    for i in range(n):
        for j in range(i + 1, n):
            if len(set(top_df['nplets'].iloc[i]).intersection(set(top_df['nplets'].iloc[j]))) == 2:
                H[i, j] = 1
                H[j, i] = 1  # Matrix is symmetric

    return top_df, H

import networkx as nx
import pandas as pd
from scipy.stats import zscore

def HO_cent_df(hypergraph, dataframe):
    """
    Calculate various centrality measures for a hypergraph and return a DataFrame.

    Parameters:
    hypergraph (numpy array): A numpy array representing the hypergraph.
    dataframe (pandas DataFrame): A DataFrame that contains the 'nplets' column.

    Returns:
    pandas DataFrame: A DataFrame with eigenvector centrality (EC),
                      betweenness centrality (BC), degree centrality (DC),
                      and their respective z-scores, along with 'nplets'.
    """

    # Convert the numpy array hypergraph to a NetworkX graph
    HG = nx.from_numpy_array(hypergraph)

    # Calculate eigenvector centrality (EC)
    EC = list(nx.eigenvector_centrality_numpy(HG).values())

    # Calculate betweenness centrality (BC)
    BC = list(nx.betweenness_centrality(HG).values())

    # Calculate degree centrality (DC)
    DC = list(nx.degree_centrality(HG).values())

    # Create a DataFrame from the centrality measures
    HO_cent = pd.DataFrame(list(zip(EC, BC, DC)), columns=['EC', 'BC', 'DC'])

    

    # Calculate z-scores for the centrality measures
    HO_cent['EC_z'] = zscore(HO_cent['EC'])
    HO_cent['BC_z'] = zscore(HO_cent['BC'])
    HO_cent['DC_z'] = zscore(HO_cent['DC'])
    
    # Add 'nplets' column from the input DataFrame
    HO_cent['nplets'] = dataframe['nplets'].to_list()

    return HO_cent

# Assuming the create_hypergraph and HO_cent_df functions are defined as previously discussed



import numpy as np
import pandas as pd
import ast
import networkx as nx
from scipy.stats import zscore
import concurrent.futures

# Assuming create_hypergraph and HO_cent_df functions are defined as previously discussed

def parallel_process(dataframe, num_hypergraphs, max_workers=None):
    centrality_results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(generate_and_compute_centrality, dataframe) for _ in range(num_hypergraphs)]
        for future in concurrent.futures.as_completed(futures):
            centrality_results.append(future.result())
    return centrality_results

def generate_and_compute_centrality(dataframe):
    top_df, H = create_hypergraph(dataframe, random_selection=True)
    centrality_df = HO_cent_df(H, top_df)
    return centrality_df

def aggregate_centrality_dataframes(centrality_dfs):
    aggregated_df = pd.concat(centrality_dfs, ignore_index=True)
    return aggregated_df

def determine_significance_threshold(centralities, p_value=0.05):
    threshold = np.percentile(centralities, 100 * (1 - p_value))
    return threshold

def main():
    # Load your dataframe
    # dataframe = pd.read_csv('your_dataframe.csv')

    num_random_hypergraphs = 1000  # Adjust based on your computational capability
    max_workers = 10  # Adjust based on your system capabilities

    # Generate and compute centralities for random hypergraphs
    centralities_random_hypergraphs = parallel_process(mean_HOI, num_random_hypergraphs, max_workers)

    # Aggregate the centralities
    aggregated_centralities = aggregate_centrality_dataframes(centralities_random_hypergraphs)

    # Save the aggregated centralities to a CSV file
    aggregated_centralities.to_csv('aggregated_centralities'+str(num_random_hypergraphs)+'copies0005fraction.csv', index=False)

    
    # Determine the threshold for significance
    ec_null_distribution = aggregated_centralities['EC']
    ec_threshold = determine_significance_threshold(ec_null_distribution, p_value=0.05)
    print("Eigenvector Centrality Threshold for Significance:", ec_threshold)
    bc_null_distribution = aggregated_centralities['BC']
    bc_threshold = determine_significance_threshold(bc_null_distribution, p_value=0.05)
    print("Betweeness Centrality Threshold for Significance:", bc_threshold)
    dc_null_distribution = aggregated_centralities['DC']
    dc_threshold = determine_significance_threshold(dc_null_distribution, p_value=0.05)
    print("Degree Centrality Threshold for Significance:", dc_threshold)


    
if __name__ == '__main__':
    main()






