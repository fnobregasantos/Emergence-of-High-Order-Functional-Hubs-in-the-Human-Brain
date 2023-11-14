#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This is the main code for Data Visualization of Simplicial Complexes

"""

__author__ = "Fernando Nobrega"
__contact__ = "f.nobregasantos@amsterdamumc.nl"
__date__ = "2020/10/15"
__status__ = "Production"


####################
# Review History   #
####################

# Reviewed and Updated by Eduarda Centeno 20201103


####################
# Libraries        #
####################

# Third party imports
import pandas as pd # version 1.1.3
import plotly.graph_objs as go # version 4.6.0 
import matplotlib # version 3.3.2
import numpy as np # version 1.18.5
import networkx as nx # version 2.4
import community # version 0.13
import meshio # version 4.0.16
import community.community_louvain
import plotly.express as px
import trimesh
from plotly.offline import iplot, init_notebook_mode

########################
# Pre-defined settings #
########################

init_notebook_mode(connected=True) # Define Notebook Mode

# Get names of areas
#n_rois = 116 # this is for AAL Atlas

# Pre-defined paths
#AAL_region_names_full
#path_areas = './Metadata/Region Names/AAL_region_names_full.txt'
#path_brainobj = './Figures/brain.obj'
#path_pos = './Metadata/Position/AAL_positions.txt'
#path_sub_order_names='./Metadata/subnetwork/subnet_ordernames_AAL.txt'
#path_sub_net_order_colors='./Metadata/subnetwork/subnet_order_colors_AAL.txt'
#Setting up the hoverinfo

#atlas='AAL92'
# Pre-defined paths
#AAL_region_names_full
#path_areas = './Atlases/'+atlas+'/annotation/'+atlas+'_region_names_full.txt'
#path_brainobj = './Figures/brain.obj'
#path_pos = './Atlases/AAL92/annotation/AAL92_positions.txt'
#path_sub_order_names='./Atlases/AAL92/annotation/AAL92_subnet_ordernames.txt'
#path_sub_net_order_colors='./Atlases/AAL92/annotation/AAL92_subnet_order_colors.txt'
#Setting up the hoverinfo


#atlas='Schaefer/100regions7networks'
# Pre-defined paths
#AAL_region_names_full
#path_areas = './Atlases/'+atlas+'/annotation/Schaefer2018_100Parcels_7Networks_Tian_Subcortex_S1_3T_region_names_full.txt'
#path_brainobj = './Figures/brain.obj'
#path_pos = './Atlases/'+atlas+'/annotation/Schaefer2018_100Parcels_7Networks_Tian_Subcortex_S1_3T_positions.txt'
#path_sub_order_names='./Atlases/'+atlas+'/annotation/Schaefer2018_100Parcels_7Networks_Tian_Subcortex_S1_3T_subnet_order_names.txt'
#path_sub_net_order_colors='./Atlases/'+atlas+'/annotation/Schaefer2018_100Parcels_7Networks_Tian_Subcortex_S1_3T_subnet_order_colors.txt'
#Setting up the hoverinfo


# Define a dictionary with configurations for each atlas
atlas_config = {
    'AAL92': {
        'n_rois': 92,
        'path_areas': 'Atlases/AAL92/annotation/AAL92_region_names_full.txt',
        'path_brainobj': './Figures/brain.obj',
        'path_pos': 'Atlases/AAL92/annotation/AAL92_positions.txt',
        'path_sub_order_names': 'Atlases/AAL92/annotation/AAL92_subnet_ordernames.txt',
        'path_sub_net_order_colors': 'Atlases/AAL92/annotation/AAL92_subnet_order_colors.txt'
    },
    'Schaefer100x7': {
        'n_rois': 116,
        'path_areas': 'Atlases/Schaefer/100regions7networks/annotation/Schaefer2018_100Parcels_7Networks_Tian_Subcortex_S1_3T_region_names_full.txt',
        'path_brainobj': './Figures/brain.obj',
        'path_pos': 'Atlases/Schaefer/100regions7networks/annotation/Schaefer2018_100Parcels_7Networks_Tian_Subcortex_S1_3T_positions.txt',
        'path_sub_order_names': 'Atlases/Schaefer/100regions7networks/annotation/Schaefer2018_100Parcels_7Networks_Tian_Subcortex_S1_3T_subnet_order_names.txt',
        'path_sub_net_order_colors': 'Atlases/Schaefer/100regions7networks/annotation/Schaefer2018_100Parcels_7Networks_Tian_Subcortex_S1_3T_subnet_order_colors.txt'
    },
    'Schaefer400x7': {
        'n_rois': 416,
        'path_areas': 'Atlases/Schaefer/400regions7networks/annotation/Schaefer2018_400Parcels_7Networks_Tian_Subcortex_S1_3T_region_names_full.txt',
        'path_brainobj': './Figures/brain.obj',
        'path_pos': 'Atlases/Schaefer/400regions7networks/annotation/Schaefer2018_400Parcels_7Networks_Tian_Subcortex_S1_3T_positions.txt',
        'path_sub_order_names': 'Atlases/Schaefer/400regions7networks/annotation/Schaefer2018_400Parcels_7Networks_Tian_Subcortex_S1_3T_subnet_order_names.txt',
        'path_sub_net_order_colors': 'Atlases/Schaefer/400regions7networks/annotation/Schaefer2018_400Parcels_7Networks_Tian_Subcortex_S1_3T_subnet_order_colors.txt'
    },
    'Schaefer1000x7': {
        'n_rois': 1016,
        'path_areas': 'Atlases/Schaefer/1000regions7networks/annotation/Schaefer2018_1000Parcels_7Networks_Tian_Subcortex_S1_3T_region_names_full.txt',
        'path_brainobj': './Figures/brain.obj',
        'path_pos': 'Atlases/Schaefer/1000regions7networks/annotation/Schaefer2018_1000Parcels_7Networks_Tian_Subcortex_S1_3T_positions.txt',
        'path_sub_order_names': 'Atlases/Schaefer/1000regions7networks/annotation/Schaefer2018_1000Parcels_7Networks_Tian_Subcortex_S1_3T_subnet_order_names.txt',
        'path_sub_net_order_colors': 'Atlases/Schaefer/1000regions7networks/annotation/Schaefer2018_1000Parcels_7Networks_Tian_Subcortex_S1_3T_subnet_order_colors.txt'
    },
    'Gordon': {
        'n_rois': 349,
        'path_areas': 'Atlases/Gordon/annotation/Gordon333_Tian_Subcortex_S1_3T_region_names_full.txt',
        'path_brainobj': './Figures/brain.obj',
        'path_pos': 'Atlases/Gordon/annotation/Gordon333_Tian_Subcortex_S1_3T_positions.txt',
        'path_sub_order_names': 'Atlases/Gordon/annotation/Gordon333_Tian_Subcortex_S1_3T_subnet_order_names.txt',
        'path_sub_net_order_colors': 'Atlases/Gordon/annotation/Gordon333_Tian_Subcortex_S1_3T_subnet_order_colors.txt'
    },
    'Brainnetome': {
        'n_rois': 246,
        'path_areas': 'Atlases/Brainnetome/annotation/BNA246_region_names_full.txt',
        'path_brainobj': './Figures/brain.obj',
        'path_pos': 'Atlases/Brainnetome/annotation/BNA246_region_names_positions.txt',
        'path_sub_order_names': 'Atlases/Brainnetome/annotation/BNA246_subnet_order_names.txt',
        'path_sub_net_order_colors': 'Atlases/Brainnetome/annotation/BNA246_subnet_order_colors.txt'
    },
    'Glasser': {
        'n_rois': 379,  # Update this number based on the actual number of ROIs for the Glasser atlas
        'path_areas': 'Atlases/Glasser/annotation/GlasserFreesurfer_region_names_full.txt',
        'path_brainobj': './Figures/brain.obj',
        'path_pos': 'Atlases/Glasser/annotation/GlasserFreesurfer_positions.txt',
        'path_sub_order_names': 'Atlases/Glasser/annotation/GlasserFreesurfer_subnet_order_names.txt',
        'path_sub_net_order_colors': 'Atlases/Glasser/annotation/GlasserFreesurfer_subnet_order_colors.txt'
    }
}

# Example of selecting an atlas
#selected_atlas = 'Schaefer100x7'  # Or any other key from the atlas_config

def atlas(selected_atlas_name):
    global n_rois, path_areas, path_brainobj, path_pos, path_sub_order_names, path_sub_net_order_colors

    if selected_atlas_name in atlas_config:
        n_rois = atlas_config[selected_atlas_name]['n_rois']
        path_areas = atlas_config[selected_atlas_name]['path_areas']
        path_brainobj = atlas_config[selected_atlas_name]['path_brainobj']
        path_pos = atlas_config[selected_atlas_name]['path_pos']
        path_sub_order_names = atlas_config[selected_atlas_name]['path_sub_order_names']
        path_sub_net_order_colors = atlas_config[selected_atlas_name]['path_sub_net_order_colors']
        print(f"Atlas chosen: {selected_atlas_name}")
    else:
        print(f"Atlas {selected_atlas_name} not found in configuration.")

        
#Choose Atlas before start  
chosen_atlas='AAL92'
atlas(chosen_atlas)

# Fetching the configurations for the selected atlas
#n_rois = atlas_config[selected_atlas]['n_rois']
#path_areas = atlas_config[selected_atlas]['path_areas']
#path_brainobj = atlas_config[selected_atlas]['path_brainobj']
#path_pos = atlas_config[selected_atlas]['path_pos']
#path_sub_order_names = atlas_config[selected_atlas]['path_sub_order_names']
#path_sub_net_order_colors = atlas_config[selected_atlas]['path_sub_net_order_colors']

# Now you can use these path variables in your script



skip=True

#######################
# Running Script      #
#######################


list_areas = pd.read_csv(path_areas,header=None).values
name_areas = [list_areas[0:n_rois,0][i] for i in range(0,n_rois)] 
Meta_Names=pd.read_csv(path_sub_order_names,header=None)
Meta_Names.columns=['subnetwork']
areas = [y + "--" + x  for x in name_areas for y in Meta_Names.values[:,0].tolist()]
sub_names=pd.read_csv(path_sub_order_names,header=None).values[:,0].tolist()
Meta_Colors=pd.read_csv(path_sub_net_order_colors,header=None)
Meta_Colors.columns=['color']
subcolors=['khaki','red','orange','violet','steelblue','purple','grey']

def get_unique_atlas_colors(atlas_name, atlas_config):
    """
    Get a unique list of colors for a specified atlas, preserving the order of first appearance.

    :param atlas_name: The name of the atlas to get colors for.
    :param atlas_config: Dictionary containing configuration for each atlas.
    :return: Ordered list of unique colors for the specified atlas.
    """
    # Check if the specified atlas exists in the configuration
    if atlas_name not in atlas_config:
        raise ValueError(f"Atlas '{atlas_name}' not found in the configuration.")

    # Get the path of the color file for the specified atlas
    color_file_path = atlas_config[atlas_name]['path_sub_net_order_colors']

    # Read colors from the file and filter out duplicates
    unique_colors = []
    with open(color_file_path, 'r') as file:
        for line in file:
            color = line.strip()
            if color not in unique_colors:
                unique_colors.append(color)

    return unique_colors
subcolors=get_unique_atlas_colors(chosen_atlas, atlas_config)

## Create gray shell

#uncover=False
def shell_brain(brain_mesh):
    """Returns a brain gray shell from a fixed brain.obj file
    
    Parameters
    ----------
    brain_mesh: meshio mesh object
    
    Returns
    -------
    mesh: plotly.graph_objs._mesh3d.Mesh3d
        
    """
    vertices = brain_mesh.vertices
    triangles = brain_mesh.faces
    
    #vertices = brain_mesh.points
    #triangles = brain_mesh.cells[0][1]
    x, y, z = vertices.T
    I, J, K = triangles.T
    #showlegend=True gives the option to uncover the shell
    mesh = go.Mesh3d(x=x, y=y, z=z, color='grey', i=I, j=J, k=K, opacity=0.1,
                     hoverinfo=None,showlegend = True, name ='Brain Shell'  #colorscale=pl_mygrey, #intensity=z,
                     #flatshading=True, #showscale=False
                     )
  
    return mesh #iplot(fig)

def openatlas(path_pos = path_pos):
    """Open an atlas file with its coordinates
     
    Parameters
    ----------
    path_pos: string
        Path to the file with atlas coordinates
    
    Returns
    -------
    data: list
        A list of coordinates
          
    """
    
    positions = pd.read_csv(path_pos,header=None, delim_whitespace=True)
    
    data = [list(row.values) for _, row in positions.iterrows()]
  
    return data


def dictpos(areas, path_pos = path_pos):
    """Creates a dictionary with 3D positions for a given atlas
    This function creates a transparent shell. This is necessary for hoverinfo,
    i.e. you can find the name of the ROI using your mouse.
     
    Parameters
    ----------
    path_pos: string
        Path to the file with atlas coordinates
    
    Returns
    -------
    trace: plotly.graph_objs._mesh3d.Mesh3d
        Plotly graphical object
    x: list
        X-axis coordinates 
    y: list
        Y-axis coordinates
    z: list
        Z-axis coordinates

    """
    
    data = openatlas(path_pos)
    x=[]
    y=[]
    z=[]
    pos3d = {}
    for i in range(0, len(data)):
        pos3d[i] = (data[i][0], data[i][1], data[i][2])
        x.append(data[i][0])
        y.append(data[i][1])
        z.append(data[i][2])

    xs = []
    ys = []
    zs = []
    for i in range(0, len(data)):
        pos3d[i] = (data[i][0], data[i][1], data[i][2])
        xs.append(1.01*data[i][0])
        ys.append(1.01*data[i][1])
        zs.append(1.01*data[i][2])
   
    trace1 = go.Mesh3d(x=xs, y=ys,z=zs, alphahull=4.2, opacity=0.0005,
                       color='gray', text=areas, hoverinfo='text')
    
    return trace1, x, y, z
brain_mesh =  trimesh.load_mesh(path_brainobj) # Reading a brain.obj file

#brain_mesh =  meshio.read(path_brainobj) # Reading a brain.obj file
brain_trace = shell_brain(brain_mesh)
trace1, _, _, _ = dictpos(areas, path_pos) # Transparent shell

# Simplicial plot


data = openatlas(path_pos) # This creates a dictionary with the positions in 3D of the nodes 

x = []
y = []
z = []
pos3d = {}
for i in range(0, len(data)):
    pos3d[i] = (data[i][0], data[i][1], data[i][2])
    x.append(data[i][0])
    y.append(data[i][1])
    z.append(data[i][2])


# Define Functions ------------------------------------------------------------

def matplotlib_to_plotly(cmap, pl_entries):
    """Create matplotlib color scales for plotly 
      
    Parameters
    ----------
    cmap : colormap 
        A colormap in matplotly  - Ex: jet_cmap
    pl_entries: list
        Number of entries
    
    Returns
    -------
    pl_colorsacle: list 
        A color scale from matplotlib that is readble in ploty    
    
    """
    
    h = 1.0/(pl_entries-1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append([float(k*h), 'rgb' + str((C[0], C[1], C[2]))])

    return pl_colorscale

# Creating colormaps that are compatible with plotly 
#magma_cmap = matplotlib.cm.get_cmap('magma')
#viridis_cmap = matplotlib.cm.get_cmap('viridis')
#plasma_cmap = matplotlib.cm.get_cmap('plasma')
#jet_cmap = matplotlib.cm.get_cmap('jet')
#inferno_cmap = matplotlib.cm.get_cmap('inferno')
#Spectral_cmap = matplotlib.cm.get_cmap('Spectral')
#Dark2_cmap = matplotlib.cm.get_cmap('Dark2')

#import matplotlib  # Ensure matplotlib is imported

# Updated color map initialization
magma_cmap = matplotlib.colormaps['magma']
viridis_cmap = matplotlib.colormaps['viridis']
plasma_cmap = matplotlib.colormaps['plasma']
jet_cmap = matplotlib.colormaps['jet']
inferno_cmap = matplotlib.colormaps['inferno']
Spectral_cmap = matplotlib.colormaps['Spectral']
Dark2_cmap = matplotlib.colormaps['Dark2']

# Continue with any other color map initializations you have in the same format


# This creates a palette with 255 points.
magma = matplotlib_to_plotly(magma_cmap, 255)
viridis = matplotlib_to_plotly(viridis_cmap, 255)
plasma = matplotlib_to_plotly(plasma_cmap, 255)
jet = matplotlib_to_plotly(jet_cmap, 255)
inferno = matplotlib_to_plotly(inferno_cmap, 255)
Spectral = matplotlib_to_plotly(Spectral_cmap, 255)



def pdpos(path_pos = path_pos):
    """Creates a dictionary with 3D positions for a given atlas
    This function creates a transparent shell. This is necessary for hoverinfo,
    i.e. you can find the name of the ROI using your mouse.
     
    Parameters
    ----------
    path_pos: string
        Path to the file with atlas coordinates
    
    Returns
    -------
    trace: plotly.graph_objs._mesh3d.Mesh3d
        Plotly graphical object
    x: list
        X-axis coordinates 
    y: list
        Y-axis coordinates
    z: list
        Z-axis coordinates

    """
    
    data = openatlas(path_pos)
    x=[]
    y=[]
    z=[]
    pos3d = {}
    for i in range(0, len(data)):
        pos3d[i] = (data[i][0], data[i][1], data[i][2])
        x.append(data[i][0])
        y.append(data[i][1])
        z.append(data[i][2])
    return pd.DataFrame.from_dict(pos3d)

#Creating the position dataframe for the given Atlas
Pd_summary=pdpos().T
Pd_summary.columns = ['x', 'y', 'z']
Basis_pd=Pd_summary.join(Meta_Names).join(Meta_Colors)




def Plot_brain_Shell(brain_trace):
    """Returns a 3d plot of a Brain, where the size and colors of the nodes 
    are proportional to a given network property
    
    Parameters
    ----------
    brain_trace: plotly.graph_objs._mesh3d.Mesh3d
    
    Returns
    -------
    A plotly graphic object (go)
        
    """
        
    data = [brain_trace]
    fig = go.Figure(data=data)
    # view
    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
                  eye=dict(x=1.7, y=0.8, z=0.225))
    
    
    
    
    layout = go.Layout(autosize=True, # To export we need to make False and uncomment the details bellow
                       #width=780, #height=540, # This is to make an centered html file. To export as png, one needs to include this margin
                        #margin=go.Margin(l=5, r=5, b=5, t=0, pad=0),
                        #title='Your tittle here!!!',
                        #font=dict(size=18, color='black'), 
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        #showline=False, #zaxis=dict(title='x Axis', 
                                                     #titlefont=dict(
                                                     #family='Courier New, monospace',
                                                     #size=80, color='#7f7f7f')),
                        scene=dict(camera=camera, 
                                   xaxis=dict(nticks=5, 
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   yaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   zaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')))
                        #xaxis=dict(
                        #    title='x Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #),
                        #yaxis=dict(
                        #    title='y Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #)
                        )
                        
    
    fig = go.Figure(data=data, layout=layout) #, layout=layout)
    
    fig.update_layout(autosize=False, width=800, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, # pad=4
                                  ))
    # need to fix the bar!!
    fig.update_layout(autosize=False, width=1200*0.8, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    #fig.update_layout(autosize=False, width=1200*0.8, height=800*0.8, 
     #                 margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    fig.update_layout(font_family="calibri")

    fig.update_layout(scene=dict(xaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False), 
                                 yaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False),
                                 zaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False))) #,za
    return iplot(fig)#,image_width=4340*1.1, image_height=2620*1.1)


def listnet(property, Graph, weight=None, distance=None):
    """Computes a network property from NetworkX and return it as a list
    
    Parameters
    ----------
    property: function
        A NetworkX function for a graph metric
    
    Graph: networkx graph
    
    weight: str
        Weight parameter if graph is weighted
    
    distance: str
        Distance parameter if graph is weighted 
        (necessary for closeness centrality, for example)
    
    Returns
    ------- 
    A list with the values of the network property per node
    
    Notes
    -------
    Notice that not all Networkx properties functions have the same output, 
    so this function might not work. E.g. nx.degree
    
    """
    
    if weight == 'weight':
        m = property(Graph, weight='weight')
    elif weight == 'distance':
        m = property(Graph, weight='distance')
    elif distance == 'distance':
        m = property(Graph, distance='distance')
    else:
        m = property(Graph)

    return list(m.values())

def Plot_Brain_Mod(G, path_pos=path_pos, scale=1):
    """ Brain 3D plot with nodes according to modularity
    
    Parameters
    ----------
    G: NetworkX graph
            
    path_pos: string
        Path to the file with atlas coordinates
    
    scale: int
        Scaling factor for node size
    
    Returns
    -------
      A 3D plot with customized nodes
   
    """
      
    trace1, x, y, z = dictpos(areas, path_pos)
    sizec = 1.5 * scale #*#scale*np.array(Network_property)
    
    #part = community.best_partition(G, weight='weight')# fixing problem!!!
    part = community.community_louvain.best_partition(G,weight='weight')
    Mod_values = [part.get(node) for node in G.nodes()]
   
    colorV = Mod_values
    trace2 = go.Scatter3d(x=np.array(x),
                        y=np.array(y),
                        z=np.array(z),
                        mode='markers',
                        marker=dict(sizemode='diameter', symbol='circle',
                                    showscale=True,
                                    colorbar=dict(title='Values',
                                                    thickness=30, x=0.1,#0.95,
                                                    len=0.8,
                                                    tickmode='array',
                                                    tickvals=colorV),
                                    opacity=0.85, size=10*sizec, color=colorV, 
                                    colorscale=Spectral, cauto=False, 
                                    cmin=np.min(colorV), cmax=np.max(colorV)),
                        showlegend=False, text=None, hoverinfo=None)
    
    data = [brain_trace, trace1, trace2]
    fig = go.Figure(data=data)
    # view
    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
                  eye=dict(x=1.7, y=0.8, z=0.225))
    
    
    
    
    layout = go.Layout(autosize=True, # To export we need to make False and uncomment the details bellow
                       #width=780, #height=540, # This is to make an centered html file. To export as png, one needs to include this margin
                        #margin=go.Margin(l=5, r=5, b=5, t=0, pad=0),
                        title='Modularity',
                        #font=dict(size=18, color='black'), 
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        #showline=False, #zaxis=dict(title='x Axis', 
                                                     #titlefont=dict(
                                                     #family='Courier New, monospace',
                                                     #size=80, color='#7f7f7f')),
                        scene=dict(camera=camera, 
                                   xaxis=dict(nticks=5, 
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   yaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   zaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')))
                        #xaxis=dict(
                        #    title='x Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #),
                        #yaxis=dict(
                        #    title='y Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #)
                        )
                        
    
    fig = go.Figure(data=data, layout=layout) #, layout=layout)
    
    fig.update_layout(autosize=False, width=800, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, # pad=4
                                  ))
    # need to fix the bar!!
    fig.update_layout(autosize=False, width=1200*0.8, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    #fig.update_layout(autosize=False, width=1200*0.8, height=800*0.8, 
     #                 margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    fig.update_layout(font_family="calibri")

    fig.update_layout(scene=dict(xaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False), 
                                 yaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False),
                                 zaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False))) #,za
    return iplot(fig)#,image_width=4340*1.1, image_height=2620*1.1)  


def G_tre(matrix, e):
    """Returns a thresholded networkx Graph from a adjacency matrix
    
    Parameters
    ----------
    matrix: matrix
        A matrix of values - connectivity matrix
    
    e: float
        Threshold value for matrix 
    
    Returns
    -------
        NetworkX graph
        
    Notes
    -------
        Calculation: (1-e) = 0.0
        
    """
    
    #"If you want to normalize just uncomment here"
    #ScdatanGA=np.array(normalize(Aut[i]))
    
    ScdatanGA = matrix
    matcopy = (np.copy(np.abs(ScdatanGA))) # be careful to always assing  copy of data, 
                                          # othewise will change the data as well
    matcopy[(np.copy(np.abs(ScdatanGA))) <= (1-e)] = 0.0
    Gfinal = nx.from_numpy_matrix(matcopy[:,:])
    
    return Gfinal


def G_den(matrix, d, verbose=False):
    """Returns a networkx Graph from a adjacency matrix, with a given density d
        
    Parameters
    ----------
    matrix: matrix
        A matrix of values - connectivity matrix
    
    d: float
        Density value for matrix binaziring 
    
    Returns
    -------
        NetworkX graph
        
    """
    
    #matrix i, density d. i is a matrix - ravel flatten the matrix
    np.fill_diagonal(matrix,0)
    temp = sorted(matrix.ravel(), reverse=True) # will flatten it and rank corr values
    size = len(matrix)
    cutoff = np.ceil(d * (size * (size-1))) # number of links with a given density
    tre = temp[int(cutoff)]
    G0 = nx.from_numpy_matrix(matrix)
    G0.remove_edges_from(list(nx.selfloop_edges(G0)))
    G1 = nx.from_numpy_matrix(matrix)
    for u,v,a in G0.edges(data=True):
        if (a.get('weight')) <= tre:
            G1.remove_edge(u, v)
    finaldensity = nx.density(G1)
    if verbose == True:
        print(finaldensity)
        
    return G1


def Plot_Brain_Prop(node_prop, path_pos=path_pos, scale=1, node_colors=None):
    """ Brain 3D plot with network property-dependent node size and color
    
    Parameters
    ----------
    node_prop: list
        A list of values with a node property
    
    path_pos: stringtr
        Path to the file with atlas coordinates
    
    scale: int
        Scaling factor for node size
    
    node_colors: list
        A list of values with a node property. Will affect node colors
    
    Returns
    -------
      A 3D plot with customized nodes
   
    """
        
    news = 1 #This is here in case we need to rescale the coordinates - not in use now
    trace1, x, y, z = dictpos(areas, path_pos)
    sizec = 2 * scale * np.array(node_prop)
    # restriction in the size
    if max(sizec)>10:
        sizec=10/max(sizec)*sizec
    if node_colors != None:
        colorV = node_colors
    else:
        colorV = np.array(node_prop)
    trace2 = go.Scatter3d(x=news*np.array(x),
                          y=news*np.array(y),
                          z=news*np.array(z),
                          mode='markers', 
                          marker=dict(sizemode='diameter',symbol='circle',
                                      showscale=True,
                                      colorbar=dict(title='Values',
                                                    thickness=30, x=0.1,#0.95,
                                                    len=0.8, tickmode = 'array',
                                                    tick0=0, dtick=1, nticks=4),
                                      opacity=1, size=10*sizec, color=colorV, 
                                      colorscale=plasma, cauto=True, 
                                      cmin=np.min(colorV), cmax=np.max(colorV)),
                          showlegend=False, text=areas, hoverinfo=None)
    data=[brain_trace, trace1, trace2]
    fig = go.Figure(data=data)
    # view
    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
                  eye=dict(x=1.7, y=0.8, z=0.225))
    
    
    
    
    layout = go.Layout(autosize=True, # To export we need to make False and uncomment the details bellow
                       #width=780, #height=540, # This is to make an centered html file. To export as png, one needs to include this margin
                        #margin=go.Margin(l=5, r=5, b=5, t=0, pad=0),
                        #title='Your tittle here',
                        #font=dict(size=18, color='black'), 
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        #showline=False, #zaxis=dict(title='x Axis', 
                                                     #titlefont=dict(
                                                     #family='Courier New, monospace',
                                                     #size=80, color='#7f7f7f')),
                        scene=dict(camera=camera, 
                                   xaxis=dict(nticks=5, 
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   yaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   zaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')))
                        #xaxis=dict(
                        #    title='x Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #),
                        #yaxis=dict(
                        #    title='y Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #)
                        )
                        
    
    fig = go.Figure(data=data, layout=layout) #, layout=layout)
    
    fig.update_layout(autosize=False, width=800, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, # pad=4
                                  ))
    # need to fix the bar!!
    fig.update_layout(autosize=False, width=1200*0.8, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    #fig.update_layout(autosize=False, width=1200*0.8, height=800*0.8, 
     #                 margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    fig.update_layout(font_family="calibri")

    fig.update_layout(scene=dict(xaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False), 
                                 yaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False),
                                 zaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False))) #,za
    return iplot(fig)#,image_width=4340*1.1, image_height=2620*1.1)    


def degree_3D(Graph, scale=1, node_colors=None, color_prop_name=None, weight=False, verbose=False):
    """This function plots one brain network, with a given treshold e
        
    Parameters
    ----------
    Graph: NetworkX graph
    
    e: float
        Threshold value for matrix 
        
    scale: int
        Scaling factor for node size
        
    node_colors: list
        Property for node colors
    
    color_prop_name: str
        Name of the property for node colors
        
    Returns
    -------
        A 3D plot
        
    """
	
    G = Graph
    value = True
    if weight==False:        
        sizec = [scale *i[1] for i in G.degree()]
        sizec = np.array(sizec) + 1
        
    else:
        sizec = [scale *i[1] for i in G.degree(weight='weight')]
        sizec = np.array(sizec) + 1
        
    if node_colors != None:
        
        colorV = node_colors
        if color_prop_name != None:
            name = color_prop_name
        else:
            name = ' '
    else:
        colorV = np.copy(sizec)
        name = 'Degree'
    scale = plasma
          
    Xed = []
    Yed = []
    Zed = []
    for edge in G.edges():
        Xed += [pos3d[edge[0]][0],pos3d[edge[1]][0], None]
        Yed += [pos3d[edge[0]][1],pos3d[edge[1]][1], None] 
        Zed += [pos3d[edge[0]][2],pos3d[edge[1]][2], None] 
        
    trace2 = go.Scatter3d(x=x, y=y, z=z, text=areas, mode='markers', #name='areas',
               marker=dict(sizemode='diameter', symbol='circle', showscale=True, 
                           colorbar=dict(title=name, thickness=30, x=0.1,#0.95,
                                         len=0.8, tickmode='linear', 
                                         tick0=0, dtick=1, showticklabels=False), opacity=0.85, 
                           size=10*sizec, color=colorV, colorscale=plasma,
                           cauto=value, cmin=0, cmax=5), hoverinfo='skip', 
               showlegend=False)  
    
    trace3 = go.Scatter3d(x=Xed, y=Yed, z=Zed, mode='lines', 
                          line=dict(color='black', width=2), 
                          hoverinfo='none', showlegend=False, opacity=0.3)

    data = [brain_trace,trace2,trace3,trace1]
    fig = go.Figure(data=data)
    # view
    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
                  eye=dict(x=1.7, y=0.8, z=0.225))
    
    
    
    
    layout = go.Layout(autosize=True, # To export we need to make False and uncomment the details bellow
                       #width=780, #height=540, # This is to make an centered html file. To export as png, one needs to include this margin
                        #margin=go.Margin(l=5, r=5, b=5, t=0, pad=0),
                        #title='Your tittle here',
                        #font=dict(size=18, color='black'), 
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        #showline=False, #zaxis=dict(title='x Axis', 
                                                     #titlefont=dict(
                                                     #family='Courier New, monospace',
                                                     #size=80, color='#7f7f7f')),
                        scene=dict(camera=camera, 
                                   xaxis=dict(nticks=5, 
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   yaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   zaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')))
                        #xaxis=dict(
                        #    title='x Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #),
                        #yaxis=dict(
                        #    title='y Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #)
                        )
                        
    
    fig = go.Figure(data=data, layout=layout) #, layout=layout)
    
    fig.update_layout(autosize=False, width=800, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, # pad=4
                                  ))
    # need to fix the bar!!
    fig.update_layout(autosize=False, width=1200*0.8, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    #fig.update_layout(autosize=False, width=1200*0.8, height=800*0.8, 
     #                 margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    fig.update_layout(font_family="calibri")

    fig.update_layout(scene=dict(xaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False), 
                                 yaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False),
                                 zaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False))) #,za
    return iplot(fig)#, image_width=4340*1.1, image_height=2620*1.1) 
    #return iplot(data)

###Check



def degree_3D_sub(Graph, scale=1, node_colors=None, color_prop_name=None, weight=False, verbose=False):
    """This function plots one brain network, with a given treshold e
        
    Parameters
    ----------
    Graph: NetworkX graph
    
    e: float
        Threshold value for matrix 
        
    scale: int
        Scaling factor for node size
        
    node_colors: list
        Property for node colors
    
    color_prop_name: str
        Name of the property for node colors
        
    Returns
    -------
        A 3D plot
        
    """



    G = Graph
    value = True
    
    if weight==False:        
        sizec = [scale *i[1] for i in G.degree()]
        sizec = np.array(sizec) + 1
        
    else:
        sizec = [scale *i[1] for i in G.degree(weight='weight')]
        sizec = np.array(sizec) + 1
    #print(sizec)
    Sz=pd.DataFrame(scale*sizec)
    Sz.columns=['size']
    Pd_plot=Basis_pd.join(Sz)
    
    if node_colors != None:
        
        colorV = Meta_Colors.values.tolist()#node_colors
        if color_prop_name != None:
            name = color_prop_name
        else:
            name = ' '
    else:
        colorV = np.copy(sizec)
        name = 'Degree'
    scale = plasma
          
    Xed = []
    Yed = []
    Zed = []
    for edge in G.edges():
        Xed += [pos3d[edge[0]][0],pos3d[edge[1]][0], None]
        Yed += [pos3d[edge[0]][1],pos3d[edge[1]][1], None] 
        Zed += [pos3d[edge[0]][2],pos3d[edge[1]][2], None] 
    
    # NEEDS TO BE ONE TRACE FOR EACH SUBNETWORK
    
    # Pseudo code: 
    # Create a dataframe with x,y,z and color
    # add trace according with the subset of the dataframe (groupby something or do it manually for each subnetwork).
    
    #df = px.data.iris()
    #fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
    #                 size='petal_length', hover_data=['petal_width'])
    #fig.show()
    # Create a dataframe where x, y, and z are collumns, than the subnetwork of the node is also a collum, and the color is also a column (like the specie in the example). Than we can do it like in the example).
    #df_grouped, x='year', y='gdpPercap', color='continent'
    #df = go.gapminder()
    #fig = go.Figure()

    #fig.add_trace(go.Bar(x=[1, 2, 3], y=[1, 3, 2]))

    #fig.show()
    #color_discrete_sequence=
    
    temp=px.scatter_3d(Pd_plot, x='x', y='y', z='z', color='subnetwork',color_discrete_sequence=subcolors,size=sizec,size_max=40)
    trace2 = temp.data
    
    #trace2 = go.Scatter3d(x=x, y=y, z=z, text=areas, mode='markers',   #name='areas',
    #           marker=dict(sizemode='diameter', symbol='circle', showscale=True, 
    #                       colorbar=dict(title=name, thickness=30, x=0.1,#0.95,
    #                                     len=0.8, tickmode='linear', 
    #                                     tick0=0, dtick=1, showticklabels=False), opacity=0.85, 
    #                       size=10*sizec, color=colorV, colorscale=plasma,
    #                       cauto=value, cmin=0, cmax=5), #hoverinfo='skip',#hoverinfo='skip', 
    #           showlegend=True,meta=nm,ids=nm,hoverinfo='all')  
    
    trace3 = go.Scatter3d(x=Xed, y=Yed, z=Zed, mode='lines', 
                          line=dict(color='black', width=2), 
                          hoverinfo='none', showlegend=True,name ='Brain Network', opacity=0.3)

    data = [brain_trace,trace2[0],trace2[1],trace2[2],trace2[3],trace2[4],trace2[5],trace2[6],trace2[7],trace3,trace1]
    fig = go.Figure(data=data)
    # view
    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
                  eye=dict(x=1.7, y=0.8, z=0.225))
    
    
    
    
    layout = go.Layout(autosize=True, # To export we need to make False and uncomment the details bellow
                       #width=780, #height=540, # This is to make an centered html file. To export as png, one needs to include this margin
                        #margin=go.Margin(l=5, r=5, b=5, t=0, pad=0),
                        #title='Your tittle here',
                        #font=dict(size=18, color='black'), 
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        #showline=False, #zaxis=dict(title='x Axis', 
                                                     #titlefont=dict(
                                                     #family='Courier New, monospace',
                                                     #size=80, color='#7f7f7f')),
                        scene=dict(camera=camera, 
                                   xaxis=dict(nticks=5, 
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   yaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   zaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')))
                        #xaxis=dict(
                        #    title='x Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #),
                        #yaxis=dict(
                        #    title='y Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #)
                        )
                        
    
    fig = go.Figure(data=data, layout=layout) #, layout=layout)
    
    fig.update_layout(autosize=False, width=800, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, # pad=4
                                  ))
    # need to fix the bar!!
    fig.update_layout(autosize=False, width=1200*0.8, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    #fig.update_layout(autosize=False, width=1200*0.8, height=800*0.8, 
     #                 margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    fig.update_layout(font_family="calibri")

    fig.update_layout(scene=dict(xaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False), 
                                 yaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False),
                                 zaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False))) #,za
    return iplot(fig)#, image_width=4340*1.1, image_height=2620*1.1) 
    #return iplot(data)


    
    
    
def Allnodeslistak(Graph, cl, verbose=False):
    """ This function returns the nodal participation in k-cliques (in percentage) 
    
    Parameters
    ----------
    Graph: NetworkX graph
    
    cl: int
        Clique size
        
    scale: int
        Scaling factor for node size
        
    Returns
    -------
    final: list
        A list with the participation in k-cliques per node (in percentage)
        
    """
    # I would like to clean this function better later on!!!
    def DIAGNOSTIC(*params) :
        if verbose : print(*params)

    # I want that the output is a vector analogous with the previous one, but for a given k, not for all k
    
    G = Graph #Graph_thresh(e,i)  # This is the initial Graph
    temp = list(nx.enumerate_all_cliques(G))
    
    DIAGNOSTIC('These are all cliques')
    DIAGNOSTIC(temp)
    
    "This lista is a vector V where each v_i is the number of cliques of size i"
    list_1 = []
    
    # We assume that the size of the cliques are smaller than 20, 
    # so we create an empty list of size 20 for the list_1
    for i in G.nodes():
        list_1.append([0] * 20) # creating a list of lists - all empty for the Scores of everybody
    
    #DIAGNOSTIC(lista)#print(list)# here I can change - Creating a list
    #test=cliques(e,i)
    #score=0
        
    "Now we run over all nodes checking if the node is in one clique or another"
    for node in G.nodes(): # now I have to do the process for is in clique
        score = 0 # This is the score of the node
        for clique in temp:
            k = len(clique)
            if node in clique:
                score += 1
                list_1[node][k-1] += +1
                
       # print('the node '+str(node)+' has score ='+str(score))
    total = []
    for elements in list_1:
        total.append(sum(elements))
        
    DIAGNOSTIC('This is the number of cliques each node is participating in')
    DIAGNOSTIC(total)
    
    nor = sum(total)
    nt = []
    for i in range(0, len(total)):
        nt.append(total[i]/nor)
    #vector=10000*np.array(nt)
    klist=[]
    
    DIAGNOSTIC('Now lets plot the number of k-cliques each number is participating in')
    
    for i in G.nodes():
        klist.append(list_1[i][cl-1])
        
        DIAGNOSTIC('the node ' + str(i) + ' has ' + str(cl) + ' - score =' 
                   + str(list_1[i][cl-1]))
        
    mostk = np.argsort(-np.array(klist))
    #nor=sum(total)
    #nor2=max(total)
    #nt=[]
    #nt2=[]
    #for i in range(0,len(total)):
    #    nt.append(total[i]/nor)
    #    nt2.append(total[i]/nor2)
    #most=np.argsort(-np.array(total))
    
    DIAGNOSTIC('These are the most important nodes ranked according to the k-clique score')
    DIAGNOSTIC(mostk)
    
    #def showrank():
    #DIAGNOSTIC(mostk)
    for i in mostk:
            DIAGNOSTIC('the node ' + str(i) + ' is in '+ str(klist[i]) + ' ' 
                       + str(cl)+ '-cliques')
    #    return 
    #DIAGNOSTIC(showrank())
    
    #DIAGNOSTIC(nt)
    #DIAGNOSTIC(nt2)
    #DIAGNOSTIC('The output is one vector normalizing the value from the maximum')
    DIAGNOSTIC(klist)
    
    
    #lista[i]=node i vector
    #print(temp)
    maxk=max(klist)
    totk=sum(klist)
    #np.nan_to_num(100*np.array(klist)/maxk)
    # We can do some choices: Here I choose the percentage of all cliques to plot
    final = np.nan_to_num(100*np.array(klist)/totk)
    
    return final


def Allnodeslistak2(Lista, cl, verbose=False):
    """ This function returns the nodal participation in k-cliques (in percentage) 
    
    Parameters
    ----------
    Graph: NetworkX graph
    
    cl: int
        Clique size
        
    scale: int
        Scaling factor for node size
        
    Returns
    -------
    final: list
        A list with the participation in k-cliques per node (in percentage)
        
    """
    # I would like to clean this function better later on!!!
    def DIAGNOSTIC(*params) :
        if verbose : print(*params)

    # I want that the output is a vector analogous with the previous one, but for a given k, not for all k
    
    #G = Graph #Graph_thresh(e,i)  # This is the initial Graph
    temp = Lista#list(nx.enumerate_all_cliques(G))
    
    DIAGNOSTIC('These are all cliques')
    DIAGNOSTIC(temp)
    
    "This lista is a vector V where each v_i is the number of cliques of size i"
    list_1 = []
    
    # We assume that the size of the cliques are smaller than 20, 
    # so we create an empty list of size 20 for the list_1
    for i in range(0,n_rois):# I can be better here - but it should work!!!G.nodes():
        list_1.append([0] * 20) # creating a list of lists - all empty for the Scores of everybody
    
    #DIAGNOSTIC(lista)#print(list)# here I can change - Creating a list
    #test=cliques(e,i)
    #score=0
        
    "Now we run over all nodes checking if the node is in one clique or another"
    for node in range(0,n_rois):#G.nodes(): # now I have to do the process for is in clique
        score = 0 # This is the score of the node
        for clique in temp:
            k = len(clique)
            if node in clique:
                score += 1
                list_1[node][k-1] += +1
                
       # print('the node '+str(node)+' has score ='+str(score))
    total = []
    for elements in list_1:
        total.append(sum(elements))
        
    DIAGNOSTIC('This is the number of cliques each node is participating in')
    DIAGNOSTIC(total)
    
    nor = sum(total)
    #Changed here
    #if nor==0:
    #    nor=1000
    nt = []
    for i in range(0, len(total)):
        nt.append(total[i]/nor)
    #vector=10000*np.array(nt)
    klist=[]
    
    DIAGNOSTIC('Now lets plot the number of k-cliques each number is participating in')
    
    for i in range(0,n_rois):#G.nodes():
        klist.append(list_1[i][cl-1])
        
        DIAGNOSTIC('the node ' + str(i) + ' has ' + str(cl) + ' - score =' 
                   + str(list_1[i][cl-1]))
        
    mostk = np.argsort(-np.array(klist))
    #nor=sum(total)
    #nor2=max(total)
    #nt=[]
    #nt2=[]
    #for i in range(0,len(total)):
    #    nt.append(total[i]/nor)
    #    nt2.append(total[i]/nor2)
    #most=np.argsort(-np.array(total))
    
    DIAGNOSTIC('These are the most important nodes ranked according to the k-clique score')
    DIAGNOSTIC(mostk)
    
    #def showrank():
    #DIAGNOSTIC(mostk)
    for i in mostk:
            DIAGNOSTIC('the node ' + str(i) + ' is in '+ str(klist[i]) + ' ' 
                       + str(cl)+ '-cliques')
    #    return 
    #DIAGNOSTIC(showrank())
    
    #DIAGNOSTIC(nt)
    #DIAGNOSTIC(nt2)
    #DIAGNOSTIC('The output is one vector normalizing the value from the maximum')
    DIAGNOSTIC(klist)
    
    
    #lista[i]=node i vector
    #print(temp)
    maxk=max(klist)
    totk=sum(klist)
    #np.nan_to_num(100*np.array(klist)/maxk)
    # We can do some choices: Here I choose the percentage of all cliques to plot
    final = np.nan_to_num(100*np.array(klist)/totk)
    
    return final


def tracenodek(Graph, k):
    """This is an intermediate function to plot the participation in cliques
    
    Parameters
    ----------
    Graph: NetworkX graph
    
    k: int
        Clique size

    Returns
    -------
    trace2 = plotly.graph_objs._scatter3d.Scatter3d
        Plotly graphical object
        
    """
    
    effsize = 1.8
    if k == 4:
        effsize = 1.2
    sizec = effsize * Allnodeslistak(Graph, k, verbose=False)# Before was e,i 
    if max(sizec)>10:
        sizec=10/max(sizec)*sizec
    value = True
    colorV = sizec
    #scale=magma
    # NEED TO ADJUST HERE - SINCE WE CAN NOT CHECK HERE THE THRESHOLD ETC!!
    check = np.mean(list(dict(Graph.degree).values()))
    if check == 0.0:
        sizec = len(sizec) * [10]
        value = False
        sizec == len(sizec) * ['darkblue']
        colorV = len(colorV) * [0]#'darkblue'
    #    #scale=[[0, 'darkblue'], [1, 'red']]#, [1.0, 'rgb(0, 0, 255)']]
        
    trace2 = go.Scatter3d(x=x, y=y, z=z, text=areas, mode='markers', #name='areas',
                          marker=dict(sizemode='diameter', symbol='circle',
                                      showscale=True, size=7*sizec,
                                      colorbar = dict(title = '% of ' + str(k) 
                                                      + '-point interactions',
                                                      thickness=30, x=0.1,
                                                      len=0.8), opacity=1,
                             #color=group,
                             #colorscale='Viridis',
                             #line=dict(color='rgb(50,50,50)', width=0.5)
                             #),
                           color=colorV, colorscale=plasma, cauto=value, cmin=0, cmax=5), 
                           hoverinfo='skip', showlegend=False #name=[i for i in areas]
                           #colorbar = dict(title = 'Life<br>Expectancy'),),
                           #color=group,
                           #colorscale='Viridis',
                           #line=dict(color='rgb(50,50,50)', width=0.5)),
                           #text=labels,
                           #hoverinfo='text'
                           #colorbar=dict(thickness=15,title='random')
                           )
    return trace2   

def tracenodek_sub(Graph, k):
    """This is an intermediate function to plot the participation in cliques
    
    Parameters
    ----------
    Graph: NetworkX graph
    
    k: int
        Clique size

    Returns
    -------
    trace2 = plotly.graph_objs._scatter3d.Scatter3d
        Plotly graphical object
        
    """
    
    effsize = 1.8
    if k == 4:
        effsize = 1.2
    sizec = effsize * Allnodeslistak(Graph, k, verbose=False)# Before was e,i 
    if max(sizec)>10:
        sizec=10/max(sizec)*sizec
    value = True
    colorV = sizec
    #scale=magma
    # NEED TO ADJUST HERE - SINCE WE CAN NOT CHECK HERE THE THRESHOLD ETC!!
    check = np.mean(list(dict(Graph.degree).values()))
    if check == 0.0:
        sizec = len(sizec) * [10]
        value = False
        sizec == len(sizec) * ['darkblue']
        colorV = len(colorV) * [0]#'darkblue'
    #    #scale=[[0, 'darkblue'], [1, 'red']]#, [1.0, 'rgb(0, 0, 255)']]
    
    
    temp=px.scatter_3d(Basis_pd, x='x', y='y', z='z', color='subnetwork',color_discrete_sequence=subcolors,size=sizec,size_max=80)
    trace2 = temp.data
    
    
    
    #trace2 = go.Scatter3d(x=x, y=y, z=z, text=areas, mode='markers', #name='areas',
    #                      marker=dict(sizemode='diameter', symbol='circle',
    #                                  showscale=True, size=7*sizec,
    #                                  colorbar = dict(title = '% of ' + str(k) 
    #                                                  + '-point interactions',
    #                                                  thickness=30, x=0.1,
    #                                                  len=0.8), opacity=1,
                             #color=group,
                             #colorscale='Viridis',
                             #line=dict(color='rgb(50,50,50)', width=0.5)
                             #),
    #                       color=colorV, colorscale=plasma, cauto=value, cmin=0, cmax=5), 
    #                       hoverinfo='skip', showlegend=False #name=[i for i in areas]
                           #colorbar = dict(title = 'Life<br>Expectancy'),),
                           #color=group,
                           #colorscale='Viridis',
                           #line=dict(color='rgb(50,50,50)', width=0.5)),
                           #text=labels,
                           #hoverinfo='text'
                           #colorbar=dict(thickness=15,title='random')
  #                         )
    return trace2   


def tracenodek_sub2(Lista, k):
    """This is an intermediate function to plot the participation in cliques
    
    Parameters
    ----------
    Graph: NetworkX graph
    
    k: int
        Clique size

    Returns
    -------
    trace2 = plotly.graph_objs._scatter3d.Scatter3d
        Plotly graphical object
        
    """
    
    effsize = 1.8
    if k == 4:
        effsize = 1.2
    sizec = effsize * Allnodeslistak2(Lista, k, verbose=False)# Before was e,i 
    if max(sizec)>10:
        sizec=10/max(sizec)*sizec
    value = True
    colorV = sizec
    #scale=magma
    # NEED TO ADJUST HERE - SINCE WE CAN NOT CHECK HERE THE THRESHOLD ETC!!
    ##check = np.mean(list(dict(Graph.degree).values()))
    #if check == 0.0:
    #    sizec = len(sizec) * [10]
    #    value = False
    #    sizec == len(sizec) * ['darkblue']
    ##    colorV = len(colorV) * [0]#'darkblue'
    #    #scale=[[0, 'darkblue'], [1, 'red']]#, [1.0, 'rgb(0, 0, 255)']]
    
    
    temp=px.scatter_3d(Basis_pd, x='x', y='y', z='z', color='subnetwork',color_discrete_sequence=subcolors,size=sizec,size_max=100)
    trace2 = temp.data
    
    
    
    #trace2 = go.Scatter3d(x=x, y=y, z=z, text=areas, mode='markers', #name='areas',
    #                      marker=dict(sizemode='diameter', symbol='circle',
    #                                  showscale=True, size=7*sizec,
    #                                  colorbar = dict(title = '% of ' + str(k) 
    #                                                  + '-point interactions',
    #                                                  thickness=30, x=0.1,
    #                                                  len=0.8), opacity=1,
                             #color=group,
                             #colorscale='Viridis',
                             #line=dict(color='rgb(50,50,50)', width=0.5)
                             #),
    #                       color=colorV, colorscale=plasma, cauto=value, cmin=0, cmax=5), 
    #                       hoverinfo='skip', showlegend=False #name=[i for i in areas]
                           #colorbar = dict(title = 'Life<br>Expectancy'),),
                           #color=group,
                           #colorscale='Viridis',
                           #line=dict(color='rgb(50,50,50)', width=0.5)),
                           #text=labels,
                           #hoverinfo='text'
                           #colorbar=dict(thickness=15,title='random')
  #                         )
    return trace2   

def plotclique3dk(Graph, e, k, t, movie=False):
    """Creates a 3D plot of the k-cliques in a brain network for a given threshold
    
    Parameters
    ----------
    Graph: NetworkX graph
    
    e: float
        Threshold value for matrix (only for plot title)
    
    k: int
        Clique size
        
    t: float or int
         transparency
    
    movie: bool , default=False

    Returns
    -------
    trace2 = plotly.graph_objs._scatter3d.Scatter3d
        Plotly graphical object
   
    """

    G = Graph
    trace2 = tracenodek(Graph,k) #tracenodek(e,i,k)
    temp = list(nx.enumerate_all_cliques(G))

    coor = []
    for i in range(0, len(temp)): #Running over all cliques
        # Create a vector with the positions for each clique
        xk = [] 
        yk = []
        zk = []
        for j in range(0, len(temp[i])):
            # including the positions of the cliques
            xk.append((pos3d[temp[i][j]][0]))
            yk.append((pos3d[temp[i][j]][1]))
            zk.append((pos3d[temp[i][j]][2]))
            
        "We have to pertubate a bit one of the nodes to make a mesh3d object" 
        if len(xk) == k:
            xk.append((pos3d[temp[i][0]][0]+0.05))
            yk.append((pos3d[temp[i][0]][1]+0.05))
            zk.append((pos3d[temp[i][0]][2]+0.05))
            # These are the poligons
            coor.append(go.Mesh3d(x=xk, y=yk, z=zk, alphahull=0.075, opacity=t,
                                  color='blue', hoverinfo='skip', showlegend=False))
            
            # These are the lines of the cliques
            coor.append(go.Scatter3d(x=xk, y=yk, z=zk, mode='lines', 
                                     line=dict(color='black', width=2), 
                                     opacity=0.15, hoverinfo='skip', 
                                     showlegend=False))
      
    Xed=[]
    Yed=[]
    Zed=[]
    for edge in G.edges():
        Xed += [pos3d[edge[0]][0],pos3d[edge[1]][0], None]
        Yed += [pos3d[edge[0]][1],pos3d[edge[1]][1], None] 
        Zed += [pos3d[edge[0]][2],pos3d[edge[1]][2], None] 

    
    
    
    camera = dict(up = dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
                  eye=dict(x=1.7, y=0.8, z=0.225) #z=0.125,y=0.95,x=1.7
                  )
    
    layout = go.Layout(title='Node participation in '+ str(k) 
                       + '-Cliques  - Density = ' + str('%.3f' % e),
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)', 
                       scene=dict(camera=camera,
                                  xaxis=dict(nticks=5, tickfont=dict(size=16, 
                                                                     color='black')), 
                                  yaxis=dict(nticks=7, tickfont=dict(size=16, 
                                                                     color='black')),
                                  zaxis=dict(nticks=7, tickfont=dict(size=16, 
                                                                     color='black')))
                       )
                                 
    if skip==False:
        tracel = go.Scatter3d(x=[0, 40, 60,-50], y=[50,-80, -70,20], z=[-40,-25,60,75],
                          mode='text', text=['front', 'right', 'back','left'],
                          textfont=dict(family='calibri'), textposition='bottom center', 
                          hoverinfo='skip', showlegend=False)
    
    # IF YOU WANNA INCLUDE THE LINK  TOGETHER WITH THE SIMPLEXES - JUST INCLUDE THIS
    # trace3=go.Scatter3d(x=Xed,
    #            y=Yed,
    #            z=Zed,
    #            mode='lines',
    #            line=dict(color='blue', width=3),
    #            hoverinfo='none'
    #            )
    coor.append(brain_trace)
    coor.append(trace2)
    if skip==False:
        coor.append(tracel)
    coor.append(trace1)
    #coor.append(trace3)
    #data=[trace1,trace2,trace3]
    data = coor
    #print(coor)
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(autosize=False, width=1200*0.8, height=800, #before 1200*0.8, height=800*0.8, 
                      margin=dict(l=50, r=50, b=100, t=100, pad=4))

    fig.update_layout(scene=dict(xaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False), 
                                 yaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False),
                                 zaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False))) #,zaxis=dict(ticklen=20,showticklabels=False, zeroline=False))
    fig.update_layout(
    font_family="calibri",
    )
    if movie==False:
        return iplot(fig)
    
    if movie==True:
        return fig.write_image("temp.svg")
    

    
def plotclique3dk_sub(Graph, e, k, t, movie=False):
    """Creates a 3D plot of the k-cliques in a brain network for a given threshold
    
    Parameters
    ----------
    Graph: NetworkX graph
    
    e: float
        Threshold value for matrix (only for plot title)
    
    k: int
        Clique size
        
    t: float or int
         transparency
    
    movie: bool , default=False

    Returns
    -------
    trace2 = plotly.graph_objs._scatter3d.Scatter3d
        Plotly graphical object
   
    """

    G = Graph
    trace2 = tracenodek_sub(Graph,k) #tracenodek(e,i,k)
    temp = list(nx.enumerate_all_cliques(G))
    # NEED TO MAKE A SINGLE DICTIONARY FROM ALL POLYGONS - THE GO MESH OBJECT.DATA IS A DICTIONARY
    coor = []
    for i in range(0, len(temp)): #Running over all cliques
        # Create a vector with the positions for each clique
        xk = [] 
        yk = []
        zk = []
        for j in range(0, len(temp[i])):
            # including the positions of the cliques
            xk.append((pos3d[temp[i][j]][0]))
            yk.append((pos3d[temp[i][j]][1]))
            zk.append((pos3d[temp[i][j]][2]))
            
        "We have to pertubate a bit one of the nodes to make a mesh3d object" 
        if len(xk) == k:
            xk.append((pos3d[temp[i][0]][0]+0.05))
            yk.append((pos3d[temp[i][0]][1]+0.05))
            zk.append((pos3d[temp[i][0]][2]+0.05))
            # These are the poligons
            coor.append(go.Mesh3d(x=xk, y=yk, z=zk, alphahull=0.075, opacity=t,
                                  color='blue', hoverinfo='skip', showlegend=False))
            
            # These are the lines of the cliques
            coor.append(go.Scatter3d(x=xk, y=yk, z=zk, mode='lines', 
                                     line=dict(color='black', width=2), 
                                     opacity=0.15, hoverinfo='skip', 
                                     showlegend=False))
      
    Xed=[]
    Yed=[]
    Zed=[]
    for edge in G.edges():
        Xed += [pos3d[edge[0]][0],pos3d[edge[1]][0], None]
        Yed += [pos3d[edge[0]][1],pos3d[edge[1]][1], None] 
        Zed += [pos3d[edge[0]][2],pos3d[edge[1]][2], None] 

    
    
    
    camera = dict(up = dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
                  eye=dict(x=1.7, y=0.8, z=0.225) #z=0.125,y=0.95,x=1.7
                  )
    
    layout = go.Layout(title='Node participation in '+ str(k) 
                       + '-Cliques  - Density = ' + str('%.3f' % e),
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)', 
                       scene=dict(camera=camera,
                                  xaxis=dict(nticks=5, tickfont=dict(size=16, 
                                                                     color='black')), 
                                  yaxis=dict(nticks=7, tickfont=dict(size=16, 
                                                                     color='black')),
                                  zaxis=dict(nticks=7, tickfont=dict(size=16, 
                                                                     color='black')))
                       )
                                 
    if skip==False:
        tracel = go.Scatter3d(x=[0, 40, 60,-50], y=[50,-80, -70,20], z=[-40,-25,60,75],
                          mode='text', text=['front', 'right', 'back','left'],
                          textfont=dict(family='calibri'), textposition='bottom center', 
                          hoverinfo='skip', showlegend=False)
    
    # IF YOU WANNA INCLUDE THE LINK  TOGETHER WITH THE SIMPLEXES - JUST INCLUDE THIS
    # trace3=go.Scatter3d(x=Xed,
    #            y=Yed,
    #            z=Zed,
    #            mode='lines',
    #            line=dict(color='blue', width=3),
    #            hoverinfo='none'
    #            )
    coor.append(brain_trace)
    coor.append(trace2[0])
    coor.append(trace2[1])
    coor.append(trace2[2])
    coor.append(trace2[3])
    coor.append(trace2[4])
    coor.append(trace2[5])
    coor.append(trace2[6])
    #
    coor.append(trace2[7])
    
    if skip==False:
        coor.append(tracel)
    coor.append(trace1)
    #coor.append(trace3)
    #data=[trace1,trace2,trace3]
    data = coor
    #print(coor)
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(autosize=False, width=1200*0.8, height=800, #before 1200*0.8, height=800*0.8, 
                      margin=dict(l=50, r=50, b=100, t=100, pad=4))

    fig.update_layout(scene=dict(xaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False), 
                                 yaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False),
                                 zaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False))) #,zaxis=dict(ticklen=20,showticklabels=False, zeroline=False))
    fig.update_layout(
    font_family="calibri",
    )
    if movie==False:
        return fig#iplot(fig)
    
    if movie==True:
        return fig.write_image("temp.svg")
    

def plotho3dk_sub(List, k, t, with_tri=True,movie=False):
    """Creates a 3D plot of the k-cliques in a brain network for a given threshold
    
    Parameters
    ----------
    Graph: NetworkX graph
    
    e: float
        Threshold value for matrix (only for plot title)
    
    k: int
        nplet size
        
    t: float or int
         transparency
    
    movie: bool , default=False

    Returns
    -------
    trace2 = plotly.graph_objs._scatter3d.Scatter3d
        Plotly graphical object
   
    """

    #G = Graph
    trace2 = tracenodek_sub2(List,k) #tracenodek(e,i,k)
    temp = List#list(nx.enumerate_all_cliques(G))
    # NEED TO MAKE A SINGLE DICTIONARY FROM ALL POLYGONS - THE GO MESH OBJECT.DATA IS A DICTIONARY
    coor = []
    for i in range(0, len(temp)): #Running over all cliques
        # Create a vector with the positions for each clique
        xk = [] 
        yk = []
        zk = []
        for j in range(0, len(temp[i])):
            # including the positions of the cliques
            xk.append((pos3d[temp[i][j]][0]))
            yk.append((pos3d[temp[i][j]][1]))
            zk.append((pos3d[temp[i][j]][2]))
            
        "We have to pertubate a bit one of the nodes to make a mesh3d object" 
        if len(xk) == k:
            xk.append((pos3d[temp[i][0]][0]+0.05))
            yk.append((pos3d[temp[i][0]][1]+0.05))
            zk.append((pos3d[temp[i][0]][2]+0.05))
            # These are the poligons
            coor.append(go.Mesh3d(x=xk, y=yk, z=zk, alphahull=0.075, opacity=t,
                                  color='blue', hoverinfo='skip', showlegend=False))
            
            # These are the lines of the cliques
            coor.append(go.Scatter3d(x=xk, y=yk, z=zk, mode='lines', 
                                     line=dict(color='black', width=2), 
                                     opacity=0.15, hoverinfo='skip', 
                                     showlegend=False))
      
    Xed=[]
    Yed=[]
    Zed=[]
    #for edge in G.edges():
    #    Xed += [pos3d[edge[0]][0],pos3d[edge[1]][0], None]
    #    Yed += [pos3d[edge[0]][1],pos3d[edge[1]][1], None] 
    #    Zed += [pos3d[edge[0]][2],pos3d[edge[1]][2], None] 

    
    
    
    camera = dict(up = dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
                  eye=dict(x=1.7, y=0.8, z=0.225) #z=0.125,y=0.95,x=1.7
                  )
    
    layout = go.Layout(title='HOI: Node participation in '+ str(k) 
                       + '-point interactions',#  - Density = ' + str('%.3f' % e),
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)', 
                       scene=dict(camera=camera,
                                  xaxis=dict(nticks=5, tickfont=dict(size=16, 
                                                                     color='black')), 
                                  yaxis=dict(nticks=7, tickfont=dict(size=16, 
                                                                     color='black')),
                                  zaxis=dict(nticks=7, tickfont=dict(size=16, 
                                                                     color='black')))
                       )
                                 
    if skip==False:
        tracel = go.Scatter3d(x=[0, 40, 60,-50], y=[50,-80, -70,20], z=[-40,-25,60,75],
                          mode='text', text=['front', 'right', 'back','left'],
                          textfont=dict(family='calibri'), textposition='bottom center', 
                          hoverinfo='skip', showlegend=False)
    
    # IF YOU WANNA INCLUDE THE LINK  TOGETHER WITH THE SIMPLEXES - JUST INCLUDE THIS
    # trace3=go.Scatter3d(x=Xed,
    #            y=Yed,
    #            z=Zed,
    #            mode='lines',
    #            line=dict(color='blue', width=3),
    #            hoverinfo='none'
    #            )
    if with_tri==False:
        #del corr
        coor = []
    
    coor.append(brain_trace)
    coor.append(trace2[0])
    coor.append(trace2[1])
    coor.append(trace2[2])
    coor.append(trace2[3])
    coor.append(trace2[4])
    coor.append(trace2[5])
    coor.append(trace2[6])
    #not sure 
    coor.append(trace2[7])
    if skip==False:
        coor.append(tracel)
    coor.append(trace1)
    #coor.append(trace3)
    #data=[trace1,trace2,trace3]
    data = coor
    #print(coor)
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(autosize=False, width=1200*0.8, height=800, #before 1200*0.8, height=800*0.8, 
                      margin=dict(l=50, r=50, b=100, t=100, pad=4))
    #fig.update_traces(marker=dict(size=12))
    #fig.update_traces(marker={'size': 15})
    fig.update_layout(scene=dict(xaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False), 
                                 yaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False),
                                 zaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False))) #,zaxis=dict(ticklen=20,showticklabels=False, zeroline=False))
    fig.update_layout(
    font_family="calibri",
    )
    if movie==False:
        return iplot(fig)
    
    if movie==True:
        return fig#.write_html(figname)#fig.write_image("temp.svg")
    
def Curv_calc(Graph, verbose=False): 
    """This function computes the curvature distribution of a given network
    
    Parameters
    ----------
    Graph: NetworkX graph
    
    Returns
    -------
    final: array 
        Array with the curvature value per node in the network
        
    """
    def DIAGNOSTIC(*params) :
        if verbose : print(*params)
        
    DIAGNOSTIC('This function run over all nodes and computes the curvature of the nodes in the graph' )
   
    G = Graph #Graph_thresh(e,i)  # This is the initial Graph
    temp=list(nx.enumerate_all_cliques(G))
    "This lista is a vector V where each v_i is the number of cliques of size i"
    list_1 = []
    
    "We suppose that the size of the cliques are smaller than 20, so we create an empty list of size 20 for the lista"
    for i in G.nodes():
        list_1.append([0] * 20) # creating a list of lists - all empty for the Scores of everybody
    
    DIAGNOSTIC('These are all cliques of the Network:')
    DIAGNOSTIC(temp)# here I can change - Creating a list
    
    #test=cliques(e,i)
    #score=0
    
    "Now we run over all nodes checking if the node is in one clique or another"
    DIAGNOSTIC('We now print the curvature score of each node in the network')
    
    for node in G.nodes(): # now I have to do the process for is in clique
        score=0 # This is the score of the node
        for clique in temp:
            k=len(clique)
            if node in clique:
                score += 1
                list_1[node][k-1] += (-1)**(k+1)*1/k
                
        DIAGNOSTIC('The node ' + str(node) + ' has curvature score =' + str(score))
        
    total = []
    for elements in list_1:
        total.append(sum(elements)) # This is good if one wants to normalize
    
    DIAGNOSTIC(total)
    
    nor = sum(total)
    nor2 = max(total)
    nt = []
    nt2 = []
    for i in range(0, len(total)):
        nt.append(total[i]/nor)
        nt2.append(total[i]/nor2)
    most = np.argsort(-np.array(total))#
    
    #def showrank():
    for i in most:
            DIAGNOSTIC('the node ' +str(i)+ ' is in '+ str(total[i])+ ' cliques')
    
    #DIAGNOSTIC(showrank())
    DIAGNOSTIC('These are the most important nodes ranked according to the total clique score')
    DIAGNOSTIC(most)
    DIAGNOSTIC('These is the array nt')

    DIAGNOSTIC(nt)
    DIAGNOSTIC('These is the array nt2')

    DIAGNOSTIC(nt2)
    DIAGNOSTIC('These is the array lista')

    DIAGNOSTIC(list_1)
    DIAGNOSTIC('The output is one vector normalizing the value from the maximum')
    " nor2 is the maximum- The output nt2 is in percentage - That means the max get 100 and the rest bet 0-100"
    
    curv = []
    for i in range(0, len(list_1)):
        curv.append(sum(list_1[i]))
        
    final = np.array(curv)
    
    return final



def plotcurv(Graph, e, movie=False):
    """Plot curvature distribution of a networkx object for a given threshold
    
    Parameters
    ----------
    Graph: NetworkX graph
    
    e: float
        Threshold value for matrix (only for plot title)
    
    movie: bool , default=False

    Returns
    -------
    Curvature plot
    
    """
    
    xi=[]
    yi=[]
    zi=[]
    for key, value in pos3d.items():
        xi.append(value[0])
        yi.append(value[1])
        zi.append(value[2])
        
    sig = Curv_calc(Graph,verbose=False)
    cut = 0.00*np.max(abs(sig))
    
    # This are the nodes with positive curvature
    pxi = []
    pyi = []
    pzi = []
    for key, value in pos3d.items():
        if sig[key] > cut:
            pxi.append(value[0])
            pyi.append(value[1])
            pzi.append(value[2])
    
    nxi = []
    nyi = []
    nzi = []
    for key, value in pos3d.items():
        # These are the nodes with negative curvatures
        if sig[key] < -cut:
            nxi.append(value[0])
            nyi.append(value[1])
            nzi.append(value[2])

    zxi = []
    zyi = []
    zzi = []
    for key, value in pos3d.items():
        #These nodes are the ones with zero curvature
        if (sig[key] < cut and sig[key] > -cut):
            zxi.append(value[0])
            zyi.append(value[1])
            zzi.append(value[2])
       
    # This is the size of the node
    size = 20 * np.abs(np.copy(sig))
       
    tracecurv = go.Scatter3d(x=xi, y=yi, z=zi, mode='markers', #name='actors',
                             marker=dict(sizemode='diameter', symbol='circle',
                                         showscale=True, 
                                         colorbar=dict(title='Node curvature', 
                                                       thickness=30,x=0.1,#before was 0.95
                                                       len=0.8), 
                                         opacity=1, size=size, color=sig, 
                                         colorscale=plasma),
                             hoverinfo='skip', showlegend=False)
    
    #tracen=go.Scatter3d(mode='text',x=nxi,
    #           y=nyi,
    #           z=nzi,
    #           text: len(nxi)*['-'],
    #           #name='actors',
     #          textfont: {size: 20}
               #marker=dict(sizemode='diameter',symbol='-',showscale=True,
                #             size=30),#color=sizec,colorscale = 'Jet'),
     #           )
    # This is the plot of the negative signs
    tracen = go.Scatter3d(x=nxi, y=nyi, z=nzi, mode='text', text=len(nxi)*['-'], 
                        textposition='middle center', 
                        textfont=dict(family='sans serif', size=30, color='black'),
                        hoverinfo='skip', showlegend=False)#)#textfont: {size: 20}}])
    
    # This is the plot of the positive signs
    tracep = go.Scatter3d(x=pxi, y=pyi, z=pzi, mode='text', text=len(pxi)*['+'],
                          textposition='middle center',
                          textfont=dict(family='sans serif', size=20, color='black'),
                          hoverinfo='skip', showlegend=False)#),textfont: {size: 20}}])

    if skip==False:
        tracel = go.Scatter3d(x=[0, 40, 60,-50], y=[50,-80, -70,20], z=[-40,-25,60,75], 
                          mode='text', #name='Markers and Text',
                          text=['front', 'right', 'back','left'], 
                          textfont=dict(family='calibri'),
                          textposition='bottom center', hoverinfo='skip', 
                          showlegend=False)
    
        data = [brain_trace, trace1, tracecurv, tracep, tracen, tracel]
    data = [brain_trace, trace1, tracecurv, tracep, tracen]
    
    # view
    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
                  eye=dict(x=1.7, y=0.8, z=0.225))
    
    
    
    
    layout = go.Layout(autosize=True, # To export we need to make False and uncomment the details bellow
                       #width=780, #height=540, # This is to make an centered html file. To export as png, one needs to include this margin
                        #margin=go.Margin(l=5, r=5, b=5, t=0, pad=0),
                        title='Node Curvature - Density = ' + str('%.3f' % e),
                        #font=dict(size=18, color='black'), 
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        #showline=False, #zaxis=dict(title='x Axis', 
                                                     #titlefont=dict(
                                                     #family='Courier New, monospace',
                                                     #size=80, color='#7f7f7f')),
                        scene=dict(camera=camera, 
                                   xaxis=dict(nticks=5, 
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   yaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   zaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')))
                        #xaxis=dict(
                        #    title='x Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #),
                        #yaxis=dict(
                        #    title='y Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #)
                        )
                        
    
    fig = go.Figure(data=data, layout=layout) #, layout=layout)
    
    fig.update_layout(autosize=False, width=800, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, # pad=4
                                  ))
    # need to fix the bar!!
    fig.update_layout(autosize=False, width=1200*0.8, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    #fig.update_layout(autosize=False, width=1200*0.8, height=800*0.8, 
     #                 margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    fig.update_layout(font_family="calibri")

    fig.update_layout(scene=dict(xaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False), 
                                 yaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False),
                                 zaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False))) #,zaxis=dict(ticklen=20,showticklabels=False, zeroline=False))
    
    if movie == False:
        return iplot(fig)
    
    if movie == True:
        #return figif movie==True:
        return fig.write_image("temp.svg")
    

    
def plotcurv_sub(Graph, e, movie=False):
    """Plot curvature distribution of a networkx object for a given threshold
    
    Parameters
    ----------
    Graph: NetworkX graph
    
    e: float
        Threshold value for matrix (only for plot title)
    
    movie: bool , default=False

    Returns
    -------
    Curvature plot
    
    """
    
    xi=[]
    yi=[]
    zi=[]
    for key, value in pos3d.items():
        xi.append(value[0])
        yi.append(value[1])
        zi.append(value[2])
        
    sig = Curv_calc(Graph,verbose=False)
    cut = 0.00*np.max(abs(sig))
    
    # This are the nodes with positive curvature
    pxi = []
    pyi = []
    pzi = []
    for key, value in pos3d.items():
        if sig[key] > cut:
            pxi.append(value[0])
            pyi.append(value[1])
            pzi.append(value[2])
    
    nxi = []
    nyi = []
    nzi = []
    for key, value in pos3d.items():
        # These are the nodes with negative curvatures
        if sig[key] < -cut:
            nxi.append(value[0])
            nyi.append(value[1])
            nzi.append(value[2])

    zxi = []
    zyi = []
    zzi = []
    for key, value in pos3d.items():
        #These nodes are the ones with zero curvature
        if (sig[key] < cut and sig[key] > -cut):
            zxi.append(value[0])
            zyi.append(value[1])
            zzi.append(value[2])
       
    # This is the size of the node
    size = 20 * np.abs(np.copy(sig))
    
    temp=px.scatter_3d(Basis_pd, x='x', y='y', z='z', color='subnetwork',color_discrete_sequence=subcolors,size=size,size_max=80)
    tracecurv = temp.data
    # THIS I HAVE TO CHANGE
    #tracecurv = go.Scatter3d(x=xi, y=yi, z=zi, mode='markers', #name='actors',
    #                         marker=dict(sizemode='diameter', symbol='circle',
    #                                     showscale=True, 
    #                                     colorbar=dict(title='Node curvature', 
    #                                                   thickness=30,x=0.1,#before was 0.95
    #                                                   len=0.8), 
    #                                     opacity=1, size=size, color=sig, 
    #                                     colorscale=plasma),
    #                         hoverinfo='skip', showlegend=False)
    
    #tracen=go.Scatter3d(mode='text',x=nxi,
    #           y=nyi,
    #           z=nzi,
    #           text: len(nxi)*['-'],
    #           #name='actors',
     #          textfont: {size: 20}
               #marker=dict(sizemode='diameter',symbol='-',showscale=True,
                #             size=30),#color=sizec,colorscale = 'Jet'),
     #           )
    # This is the plot of the negative signs
    tracen = go.Scatter3d(x=nxi, y=nyi, z=nzi, mode='text', text=len(nxi)*['-'], 
                        textposition='middle center', 
                        textfont=dict(family='sans serif', size=30, color='black'),
                        hoverinfo='skip', showlegend=True,name="-")#)#textfont: {size: 20}}])
    
    # This is the plot of the zero signs
    tracez = go.Scatter3d(x=zxi, y=zyi, z=zzi, mode='text', text=len(pxi)*['0'],
                          textposition='middle center',
                          textfont=dict(family='sans serif', size=20, color='black'),
                          hoverinfo='skip', showlegend=False)#),textfont: {size: 20}}])
    
    # This is the plot of the positive signs
    tracep = go.Scatter3d(x=pxi, y=pyi, z=pzi, mode='text', text=len(pxi)*['+'],
                          textposition='middle center',
                          textfont=dict(family='sans serif', size=20, color='black'),
                          hoverinfo='skip', showlegend=True,name="+")#),textfont: {size: 20}}])
    

    if skip==False:
        tracel = go.Scatter3d(x=[0, 40, 60,-50], y=[50,-80, -70,20], z=[-40,-25,60,75], 
                          mode='text', #name='Markers and Text',
                          text=['front', 'right', 'back','left'], 
                          textfont=dict(family='calibri'),
                          textposition='bottom center', hoverinfo='skip', 
                          showlegend=False)
    
        data = [brain_trace, trace1, tracecurv[0],tracecurv[1],tracecurv[2],tracecurv[3],tracecurv[4],tracecurv[5],tracecurv[6], tracep, tracen,tracez, tracel]
    data = [brain_trace, trace1, tracecurv[0],tracecurv[1],tracecurv[2],tracecurv[3],tracecurv[4],tracecurv[5],tracecurv[6], tracep, tracen,tracez]
    # view
    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
                  eye=dict(x=1.7, y=0.8, z=0.225))
    
    
    
    
    layout = go.Layout(autosize=True, # To export we need to make False and uncomment the details bellow
                       #width=780, #height=540, # This is to make an centered html file. To export as png, one needs to include this margin
                        #margin=go.Margin(l=5, r=5, b=5, t=0, pad=0),
                        title='Node Curvature - Density = ' + str('%.3f' % e),
                        #font=dict(size=18, color='black'), 
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        #showline=False, #zaxis=dict(title='x Axis', 
                                                     #titlefont=dict(
                                                     #family='Courier New, monospace',
                                                     #size=80, color='#7f7f7f')),
                        scene=dict(camera=camera, 
                                   xaxis=dict(nticks=5, 
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   yaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')),
                                   zaxis=dict(nticks=7,
                                              #title='x', 
                                              #titlefont=dict(
                                                              #family='Courier New, monospace',
                                                              #size=40,
                                                              #color='#7f7f7f'), 
                                              tickfont=dict(size=16,
                                                            color='black')))
                        #xaxis=dict(
                        #    title='x Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #),
                        #yaxis=dict(
                        #    title='y Axis',
                        #    titlefont=dict(
                        #        family='Courier New, monospace',
                        #        size=18,
                        #        color='#7f7f7f'
                        #    )
                        #)
                        )
                        
    
    fig = go.Figure(data=data, layout=layout) #, layout=layout)
    
    fig.update_layout(autosize=False, width=800, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, # pad=4
                                  ))
    # need to fix the bar!!
    fig.update_layout(autosize=False, width=1200*0.8, height=800, 
                      margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    #fig.update_layout(autosize=False, width=1200*0.8, height=800*0.8, 
     #                 margin=dict(l=50, r=50, b=100, t=100, pad=4))
    
    fig.update_layout(font_family="calibri")

    fig.update_layout(scene=dict(xaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False), 
                                 yaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False),
                                 zaxis=dict(ticklen=20, showticklabels=False, 
                                            zeroline=False, showbackground=False))) #,zaxis=dict(ticklen=20,showticklabels=False, zeroline=False))
    
    if movie == False:
        return iplot(fig)
    
    if movie == True:
        #return figif movie==True:
        return fig#.write_image("temp.svg")

    



# IF YOU WANNA OPEN DIRECTLY IN THE BROWSER USE THE COMMAND BELLOW
#(plotly.offline.plot(fig,auto_open=True))

#size=10
#for frame in range(0,size):
#    fig=plotclique3dk(G_den(matrix,frame/100),frame/100,2,0.5,movie=True)
    
#name = 'vertical is along y+z'
#    camera = dict(
#            eye=dict(x=1.8*np.sin(6.28*(frame+1)/size), y=1.8*np.cos(6.28*(frame+1)/size), z=0.1*np.sin(2*6.28*frame/size)),
    #eye=dict(x=2, y=0, z=0)
#    )
#camera = dict(
#    eye=dict(x=1.25, y=1.25, z=1.25))


#    fig.update_layout(scene_camera=camera)
#fig.show()

#    fig.write_image("Filtration/figteste"+str(frame)+".png")


    
