# Emergence-of-High-Order-Hubs-in-the-Human-Connectome
This repository has the relevant codes associated with the manuscript: Emergence of High Order Hubs in the Human Connectome. It gives instructions on how to compute multivariate information theory metrics, and how to analyse it in the context of hypergraphs, and how to visualize it.

## Data - Since HCP data is sensitive, we use a sample timeseries data.

## Code Block 1: High Order connectivity from timeseries

input: Any time series - in this case, we included a rs-fMRI time series.
output: A csv file with multiple high order connectivity metrics for all similarities metrics discussed in our manuscript.

Notice that those similarity metrics were created combining codes from multiple sources, and for our manuscript we used the codes developed in Guillaume and Pierre, combined int in the infotopo_server.py file.

That said, the final output is a pandas DataFrame with a column for each Multivariate Metric, namely, Interaction Information, Total Correlation, Oinfo, and Sinfo. 

## Code Block 2: Statistical selection of High Order links. 

We have a folder with the computed High Order connectivity for all subjects. We will use this folder to have a group level measure for the statistical selection of High Order links. We did phase randomization of each timeseries, and computed the same metrics for each subject, which is stored in a different folder. Then we ccompared, at group level, the statistical distribution of the phase randomized triplets vs the original ones.  We selected the hyperlinks that were significant in at least 95% of the subjects.

### Step 1: Loading all High Order Connectivity

### Step 2: The second Block will actually compute High order connectivity. First I will do everything at the average level. Therefore I need:

#### 1) Load all files from dropbox somehow. 
#### 2) Create the average High Order connectivity for the whole cohort. 
#### 3) Run the high-order connectivity script for everything.
#### 4) Eventually Store all HIgh order Hubs in a Dataframe (Brainstorm this a bit more).

## Code Block 3: Data Visualization of High Order Hubs in the Human connectome.

Upload of my current working code on it. It's so detailed that I will make more steps in it while doing it.

## Code Block 4: Run High Order metrics in the whole cohort.

The same has code block 3: I will be inspired by the codes I made for Rodrigo Cofre. 




