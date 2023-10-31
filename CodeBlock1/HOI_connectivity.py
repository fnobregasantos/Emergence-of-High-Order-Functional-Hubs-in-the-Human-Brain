#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 09:04:21 2022

@author: boltzmann
"""
######DESCRIPTION#####

# This is the first code block from the HOI project. It does read one rs-fMRI time series, compute the high order links, 
# and outputs a csv file with a list of n_plets for all possible HOI metrics in this manuscript. However, the list of HOI metrics can grow as well.

#Pending stuff will have a ? interrogation mark

##########
##PART 1## 
##########


#importing relevant packages, and doing settings for runneing the codes: path to data, size of the atlas, order of the run, etc.

# Link to Pierre's repository and to Guilaumes' Repository

import os
import numpy as np
#setting the current working directory
#os.chdir('/Users/boltzmann/Dropbox/VUmc/Topology_Behavior/Backup_Pierre')
#os.getcwd()
import glob
import cmath
from scipy.stats import norm
from itertools import combinations
from scipy.special import digamma
#importing Pierres Code - infotopo
import infotopo_server as infotopo
import pandas as pd

############
##SETTINGS##
############

#These are all settings/choices we have made in this project, as well as access to the data. We included everything in the top, so that is easy to adjust/finetune for further applications.

# Path to the data:
#path='/Users/boltzmann/Dropbox/VUmc/GitHub/Emergence-of-High-Order-Hubs-in-the-Human-Connectome/HCP_Data/HCP_new_LR/HCP_new_LR/*'


# Number of nodes in the High Order Network - here I've used AAL atlas, which has N=92 brain areas (nodes).
atlas_size = 92
d_max = 3


#####################
##Data and settings## 
#####################


#Accessing/importing the rs-fMRI time series

#OBS: This will change from project to project. The other steps are straightforward 
#Getting the files addresses - notice that this is a local address in my mac for now - change it for your files address
#files = glob.glob(path)
# Saving the whole Cohort in a list of DataFrames, which are 100 individuals, each individual is stored in Cohort[i]
#Obs: For saving purposes, it can be helpful to store the ids of the individuals elsewhere
#IDs=[names[-10:-4] for names in files]

#Cohort=[]
#for i in range(0,len(files)):
#    df=pd.read_csv(files[i],sep='\t',header=None)
#    df = df.iloc[:-1 , :]
    # if needed, some cleaning step could be done in this stage here
#    Cohort.append(df)

#Settings for the infotopo/Pierre's algorithm: dimension_max = Order of the interaction

information_topo = infotopo.infotopo(dimension_max = d_max,
                                     dim_to_rank = 2, number_of_max_val = 5,dimension_tot=atlas_size,
                            #dimension_tot = 92,
                            #sample_size = sample_size,
                            #work_on_transpose = work_on_transpose,
                            nb_of_values = 20,
                            #sampling_mode = sampling_mode,
                            #deformed_probability_mode = deformed_probability_mode,
                            #supervised_mode = supervised_mode,
                            forward_computation_mode = True)




##########    
##PART 2## 
##########
#Computing High Order Interdependencies

#########################
#PART2.1 Oinfo and Sinfo# 
#########################

#- Notice that Redundant core and Synergetic core are also possible as outputs.

#? Source code at:
#? link to Guillaume Github :::
#? Python translation of the code available in :::

def gaussian_ent_biascorr(N,T):

	"""
	
	INPUTS:
	
	N = Number of dimensions
	T = Sample size
	
	OUTPUTS
	
	biascorr = bias corrector value
	"""
	
	values = np.arange(1, N+1)
	
	return 0.5 * ((N * np.log(2/(T-1))) + np.sum(list(map(lambda n : digamma((T-n)/2), values))) )


def data2gaussian (data) :

	"""
	
	INPUTS :
	
	data = T samples x N variables matrix
	
	OUTPUTS :
	
	gaussian_data = T samples x N variables matrix with the gaussian copula transformed data.
	covmat = N x N covariance matrix of gaussian copula transformed data.
	
	"""
	
	T = len(data)
	sort_index = np.argsort(data, axis = 0) # Sort the data and keep the indexes.
	copdata = np.argsort(sort_index, axis = 0) # Sorting sorting indexes
	copdata += 1 # To avoid 0 because of the python indexation
	copdata = copdata/ (T+1) # Normalization.
	gaussian_data = norm.ppf(copdata, 0, 1) # PPF : Probability Density Function  => Gaussian data
	gaussian_data[~np.isfinite(gaussian_data)] = 0 # Removing -Inf
    #ask if this removal is correct or something like that
	cov_mat = np.dot(np.transpose(gaussian_data), gaussian_data ) / (T-1) # Covariance matrix
	
	return gaussian_data, cov_mat

def ent_fun (x,y):

	"""
	
	In order to avoid log(0), we replace the returned value as NaN value.
	"""
	
	if (( 2*np.pi*np.exp(1) ) ** x) * y == 0:
	
		return np.nan
	else:
		return 0.5 * cmath.log((( 2*np.pi*np.exp(1) ) ** x) * y)



def reduce_x (x, covmat):

	covmat = np.delete(covmat, x, axis = 0)
	covmat = np.delete(covmat, x, axis = 1)
	
	return covmat





def soinfo_from_covmat (covmat, T):
	
	"""
	
	INPUTS :
	
	covmat = N x N covariance matrix
	T = lenght data
	
	OUPUTS :
	
	oinfo = O - Information
	sinfo = S - Information of the system with covariance matrix 'covmat'.
	
	"""
	
	covmat = np.array(covmat)
	N = len(covmat)
	emp_det = np.linalg.det(covmat) # Determinant
	single_vars = np.diag(covmat) # Variance of single variables (Diagonal matrix values)
	
	### Bias corrector for N, (N-1) and one gaussian variables :
	
	biascorrN = gaussian_ent_biascorr(N, T)
	biascorrNmin1 = gaussian_ent_biascorr(N-1, T)
	biascorr_1 = gaussian_ent_biascorr(1, T)
	
	### Computing estimated measures for multi-variate gaussian variables :
	
	tc = np.sum(list(map(lambda x : ent_fun(1,x), single_vars)) - biascorr_1) - (ent_fun(N,emp_det) - biascorrN) #Total correlation
	
	Hred = 0
	
	for red in range(1, N+1):
		Hred += ent_fun((N-1), np.linalg.det(reduce_x(red-1, covmat))) - biascorrNmin1
		
	dtc = Hred - (N-1) * (ent_fun(N, emp_det)-biascorrN) # dtc = Dual Total Correlation

	oinfo = tc - dtc
	sinfo = tc + dtc
	
	return oinfo, sinfo



def high_order (data, n):

    """ 

    Function to compute S-Information, O-Information, and characterize the High Order	
    interactions among n variables governed by Redundancy or Synergy.
    
    INPUTS :
    
    data = Matrix with dimensionality (N,T), where N is the number of brain regions or 
    modules, and T is the number of samples.
    n = number of interactions or n-plets.
    
    OUTPUTS :
    Red = Matrix with dimension (1, Modules), with the redundancy values per patient 
    and per module.
    Syn = Matrix with dimension (1, Modules), with synergy values per patient 
    and per module.
    Oinfo = O-Information for all the n-plets.
    Sinfo = S-Information for all the n-plets.
    
    """

    ### INITIALISATION :
    
    Modules = len(data)
    Red = np.zeros(Modules) 
    Syn = np.zeros(Modules)
    
    vector = np.arange(0, Modules)
    nplets = []

        
    Oinfo = []
    Sinfo = []


    ### N-PLETS CALCULATION :
    
    for x in combinations(vector, n): # n-tuples without repetition over 20 modules
        nplets.append(x)
    nplets = np.array(nplets)

    ## DATA NORMALISATION :

    mean = np.mean(data, axis = 1)
    mean = mean.reshape(-1,1)
    
    dataNorm = data - mean

    gaussian_data, cov_mat = data2gaussian (np.transpose(dataNorm)) # Transformation to Copulas and Covariance Matrix Estimation
    
    i = 0
    
    ### OINFO AND SINFO COMPUTATION :	

    Info = []
    Info.append(list(map(lambda x : soinfo_from_covmat(cov_mat[np.ix_(x,x)], len(dataNorm[0])), nplets)))
    Info = np.transpose(Info)
    Oinfo = np.array(Info[0])
    Sinfo = np.array(Info[1])
    
    ### REDUNDANCY AND SYNERGY COMPUTATION :
    
    """
    Here, we want to verify in each nplet if a module exist : when it is the case we compute
    the associated Redundancy and Synergy, according to the Oinfo value of these nplets.
    """
    Values = []
    
    for module in range(Modules):
        Values, cols = np.where(nplets == module)
        
        Oinfo_module_pos = []
        Oinfo_module_neg = []
        
        for i in range(len(Values)):

            if Oinfo[Values[i]].real > 0 :
                Oinfo_module_pos.append(Oinfo[Values[i]].real)
            if Oinfo[Values[i]].real < 0 :
                Oinfo_module_neg.append(Oinfo[Values[i]].real)

        Red[module] = np.mean(np.array(Oinfo_module_pos))
        Syn[module] = np.mean(np.absolute(np.array(Oinfo_module_neg)))
        
        Values = []
        
    Red = Red.reshape(-1,1)
    Syn = Syn.reshape(-1,1)
    
    np.nan_to_num(Syn)
    Red= [value[0] for value in Red]
    Syn= [value[0] for value in Syn]
    Oinfo= [np.real(value[0]) for value in Oinfo]
    Sinfo= [np.real(value[0]) for value in Sinfo]
    

    return Red, Syn, Oinfo, Sinfo, nplets

def run_High_Order(N,df,save=False):
    "This code computes Oinfo, Sinfo for an individual in Cohort"
    #for individual in Cohort:
    n = N
    temp=np.transpose(df).values
    print("Experiment :")
    print("Data shape : ", np.shape(temp))
    print("N-plet : N = ", n)
    Red, Syn, Oinfo, Sinfo, nplets = high_order (temp, n)
    ROIs=list(range(0,atlas_size))
    
    High_order = pd.DataFrame(list(zip(Oinfo, Sinfo, nplets)),columns=['Oinfo','Sinfo','nplets'])

    #pd.DataFrame(High_order).to_csv('High_order_3/Red_Syn_3_'+files[i][-10:],index=False, sep=' ', na_rep = 'NaN',header=None)
    #i+=1
    return High_order


def info_topo(df):
    Data = df.dropna().to_numpy()#pd.read_csv('AAL_timeseries_100307.txt', sep ='\t',header=None).dropna().to_numpy()

   
#number_of_max_val explores the highest and lowest values of multivariate information theory

# Joint entropies
# Interaction, mutual and total correlation
    Nentropie = information_topo.simplicial_entropies_decomposition(Data)




#Geting the indexes
    indexes=list(Nentropie.keys())
    idx=[list(i) for i in indexes]
#getting the values for joint distribution
    values_joint=list(Nentropie.values())
#creating the tuples for Joint entropy
    data_tuples_Joint_S = list(zip(values_joint,idx))
#Separating it according to the size
    Joint_S=pd.DataFrame(data_tuples_Joint_S,columns=['values','index'])
    Joint_S_1= Joint_S[Joint_S['index'].str.len()==1]
    Joint_S_2= Joint_S[Joint_S['index'].str.len()==2]
    Joint_S_3= Joint_S[Joint_S['index'].str.len()==3]
#Same for Mutual Information
    Ninfomut = information_topo.simplicial_infomut_decomposition(Nentropie)
    values_mut=list(Ninfomut.values())
    data_tuples_Mut_S = list(zip(values_mut,idx))
    Mut_S=pd.DataFrame(data_tuples_Mut_S,columns=['values','index'])
    Mut_S_1= Mut_S[Mut_S['index'].str.len()==1]
    Mut_S_2= Mut_S[Mut_S['index'].str.len()==2]
    Mut_S_3= Mut_S[Mut_S['index'].str.len()==3]
#Same for Total Correlation
    TC=information_topo.total_correlation_simplicial_lanscape(Nentropie)
    values_TC=list(TC.values())
    data_tuples_TC = list(zip(values_TC,idx))
    TC_S=pd.DataFrame(data_tuples_TC,columns=['values','index'])
    TC_S_1= TC_S[TC_S['index'].str.len()==1]
    TC_S_2= TC_S[TC_S['index'].str.len()==2]
    TC_S_3= TC_S[TC_S['index'].str.len()==3]

    test=pd.concat([Joint_S_3['values'], Mut_S_3['values'],TC_S_3], axis=1, join="inner")
    test.columns=['Joint Ent','Mut Info','Total Corr','nplets']
    #pd.DataFrame(test).to_csv('Summary_High_order_3_'+files[i][-10:],index=False, sep=' ', na_rep = 'NaN',header=None)
    #i+=1
    return test


def run_all_HOI(df):#,save=False):
    # Comment - I don't realy know the reason, but I've called tuples the nplets, maybe in the future this will be helpful
    #Interaction Info and Total Correlation
    IITC=info_topo(df)
    #JointData = JointData.assign(tuples=pd.Series(nplets).values)
    # S and O Info:
    SO=run_High_Order(d_max,df)
    #BCAM=run_high
    JointData=pd.concat([SO[['Oinfo','Sinfo']].reset_index(drop=True),IITC.reset_index(drop=True)], axis=1)
    #nplets=JointData['nplets'].iloc[:, 0]
    #JointData = JointData.assign(tuples=pd.Series(nplets).values)
    #if save==True:
    #    JointData.to_csv('HOI_ID_'+str(IDs[individual])+'.csv')   
    return JointData



