# This file is used to define isolated functions for our ABM
import random as rd
import math
from Agent import *

def make_agents_connections(agent_list,amount_of_friends = 3,influencer_network = 5):
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
    edge_list : List of tuples of Agents
        The function return a List containing Tuple of Agent pairs. 
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
                    edge_list.append((c1,c2))
                
    edge_list = list(set(edge_list))
    return edge_list
