# This file is used to define isolated functions for our ABM
import random as rd
import matplotlib.pyplot as plt
from matplotlib import cm
import math
from Agent import *
import networkx as nx

def make_agent_nodes(agent_list):
    """
    A function to generate agent nodes used for the model environment

    Parameters
    ----------
    agent_list : list of agents (commoners,influencers)
        Specifies a list of agents. More explicit a list of CommonerAgents and InfluencerAgents

    Returns
    -------
    agent_nodes : List of tuples with agent ids and agents
        Ex [(0,{'agent':CommonerAgent})]
    """
    agent_nodes = [(x.agent_id,{'agent':x}) for x in agent_list]
    return agent_nodes

def make_agents_connections(agent_list,amount_of_friends = 3,influencer_network = 6):
    """
    A function that takes a list of agents and then make appropiate connections between CommonerAgents and InfluencerAgent.
    Two InfluencerAgents cannot have a connection to each other

    Parameters
    ----------
    agent_list : List of Agents
        Takes a list of CommonerAgents and InfluencerAgents
    amount_of_friends : int, optional
        Amount of connections/friends between each agent. The default is 3.
    influencer_network : int, optional
        Increase the degree of connections between InfluencerAgents and CommonerAgents. The default is 5.

    Returns
    -------
    edge_list : List of tuples of Agent ids
        The function return a List containing Tuple of Agent ids pairs. 
        To be used with the networkx library.
    """
    
    edge_list = []
    for index,agent in enumerate(agent_list):
        
        if isinstance(agent,InfluencerAgent):
            amount_of_friends = influencer_network
            amount_of_friends = amount_of_friends*influencer_network
            
        for i in range(0,amount_of_friends):
            random_agent = agent_list[rd.randint(0,len(agent_list)-1)]
            c1,c2 = (agent,random_agent)
            
            if isinstance(c1,InfluencerAgent) == True and isinstance(c2,InfluencerAgent) == True:
                continue
            else:    
                if c1.agent_id is not c2.agent_id:
                    if isinstance(c1,CommonerAgent) == True and isinstance(c2,CommonerAgent) == True:
                        homophily_weight = rd.randint(1,3)
                        edge_list.append((c1.agent_id,c2.agent_id,homophily_weight))
                    else:
                        edge_list.append((c1.agent_id,c2.agent_id,0))
                
    edge_list = list(set(edge_list))
    return edge_list

def draw_graph_environment(model,draw_labels = False):
    """
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
        Commoners: gray
        FInfluencer: red
        RInfluencer: blue
    """
    nodes = model.graph_environment._node
    
    color_map = []
    
    for key,value in nodes.items():
        if isinstance(value['agent'],CommonerAgent) == True:
            color_map.append('lightgray')
        elif isinstance(value['agent'],InfluencerAgent) == True:
            if value['agent'].agent_type == 0:
                color_map.append('blue')
            else:
                color_map.append('red')
    
    # Extra properties
    pos = nx.random_layout(model.graph_environment)
    nx.draw(model.graph_environment,pos,node_color=color_map, with_labels=True,node_size=600)
    if draw_labels == True:
        labels = nx.get_edge_attributes(model.graph_environment, 'weight')
        nx.draw_networkx_edge_labels(model.graph_environment,pos,font_size=12,edge_labels=labels)
