# This file is used to define isolated functions for our ABM
import random as rd
import matplotlib.pyplot as plt
from matplotlib import cm
import math
from Agent import *
import networkx as nx
import numpy as np

def make_agent_nodes(agent_list):
    '''
    A function to generate agent nodes used for the model environment

    Parameters
    ----------
    agent_list : list of agents (users,influencers)
        Specifies a list of agents. More explicit a list of UserAgents and InfluencerAgents

    Returns
    -------
    agent_nodes : List of tuples with agent ids and agents
        Ex [(0,{'agent':UserAgent})]
    '''
    agent_nodes = [(x.agent_id,{'agent':x}) for x in agent_list]
    return agent_nodes
    

def make_agents_connections(agent_list, user_network, influencer_network, f_network_mult_factor, homophily_weight_range):
    """
    A function that takes a list of agents and then make appropiate connections between UserAgents and InfluencerAgent.
    Two InfluencerAgents cannot have a connection to each other
    
    Specified amount of friends are not guaranteed, since there is a probability of befriending oneselve or two influencer agenter befriending each other
    in this case these friendsships are discarded

    Parameters
    ----------
    agent_list : List of Agents
        Takes a list of UserAgents and InfluencerAgents
    user_network : int, optional
        Amount of connections/friends between each agent. The default is 3.
    influencer_network : int, optional
        Increase the degree of connections between InfluencerAgents and UserAgents. The default is 5.
    homophily_weight_range: int
        Specify the weight range of the homophily relationsship between UserAgents

    Returns
    -------
    edge_list : List of tuples of Agent ids
        The function return a List containing Tuple of Agent id pairs. 
        To be used with the networkx library.
    """
    
    edge_list = []
    for index,agent in enumerate(agent_list):
        # Temporary variable for network size
        temp_network = user_network
        
        if isinstance(agent,InfluencerAgent) == True:
            temp_network = influencer_network
            if agent.agent_type == 1:   
                temp_network = round((temp_network*influencer_network) * f_network_mult_factor)
            else:
                temp_network = round(temp_network*influencer_network) 
        
        for i in range(0,temp_network):
            random_agent = agent_list[rd.randint(0,len(agent_list)-1)]
            c1,c2 = (agent,random_agent)
            
            if isinstance(c1,InfluencerAgent) and isinstance(c2,InfluencerAgent):
                continue
            else:    
                if c1.agent_id is not c2.agent_id:
                    if isinstance(c1,UserAgent) == True and isinstance(c2,UserAgent) == True:
                        homophily_weight = rd.uniform(1,homophily_weight_range)
                        edge_list.append((c1.agent_id,c2.agent_id,homophily_weight))
                    else:
                        edge_list.append((c1.agent_id,c2.agent_id,0))
                
    edge_list = list(set(edge_list))
    return edge_list



# Only for testing purpose

def draw_graph_environment(model,draw_labels = False):
    '''
    Function to draw the graph with colors and labels

    Parameters
    ----------
    model : Class model
        Takes an ABM model as parameter

    draw_labels: boolean
        If true then weights on edges will be displayed in the drawing
    
    Returns
    -------
    nx.draw()
        Draws the environment with respective colors.
        users: gray
        FInfluencer: red
        RInfluencer: blue
    '''
    nodes = model.graph_environment._node
    
    color_map = []
    
    for key,value in nodes.items():
        if isinstance(value['agent'],UserAgent) == True:
            color_map.append('lightgray')
        elif isinstance(value['agent'],InfluencerAgent) == True:
            if value['agent'].agent_type == 0:
                color_map.append('blue')
            else:
                color_map.append('red')
    
    # Extra properties
    pos = nx.random_layout(model.graph_environment)
    nx.draw(model.graph_environment,pos,node_color=color_map, with_labels=True,node_size=600,font_family="sans-serif")
    if draw_labels == True:
        labels = nx.get_edge_attributes(model.graph_environment, 'weight')
        nx.draw_networkx_edge_labels(model.graph_environment,pos,font_size=10,edge_labels=labels)

# Normal distribution with Numpy
def normalDistNP(size,mean = 0, std = 15):
    """
    Parameters
    ----------
    size : int
        insert the population size of the users in the model
    mean : int, optional
        specify the mean value. The default is 0.
    std : std, optional
        specify the standard deviation. The default is 25.

    Returns
    -------
    nd : Array of integers

    """

    nd = (np.random.normal(mean, std, size))
    nd = nd[(nd < 50) & (nd > -50)] 
    
    while len(nd) != size:
        nd = (np.random.normal(mean, std, size))
        nd = nd[(nd < 50) & (nd > -50)] 
    
    return nd

