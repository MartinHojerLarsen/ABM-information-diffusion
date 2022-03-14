# Import statements
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm
from re import I
from Agent import *
import random as rd
from Functions import *
import pandas as pd
import numpy as np
import time
#from Post import *

class Model():
    def __init__(self,population, distribution):
        # Initialize Agent list
        self.agents = []
        # Initialize population
        self.population = population
        # Initialize Graph
        self.graph_environment = nx.Graph()
        # Initialize Pd.DataFrame
        self.dataset = pd.DataFrame(columns=['Timestep','Agent Id','Agent Type','Opinion','Influence Susceptibility','Influence Factor','Network'])
        # Keeping track of timesteps
        self.timestep_val = 0
        
        commoner_dist,influencer_dist = distribution
        if commoner_dist + influencer_dist != 100:
            raise Exception("Population distribution mismatch. Must be equal to 100")

        self.commoner_population = round(self.population*(commoner_dist/100)) # Divides population into Commoners and Influencers
        self.influencer_population = round(self.population*(influencer_dist/100)) # Divides population into Commoners and Influencers

        for i in range(0,self.commoner_population):
            # create commoner agents
            agent_id = i
            agent_opinion = rd.randint(-50, 50)
            i_susceptibility = rd.uniform(1, 2)

            self.agents.append(CommonerAgent(agent_id,agent_opinion,i_susceptibility))

        for i in range(self.commoner_population,self.population):
            # create influencer agents
            agent_id = i
            influencer_type = rd.randint(0,1) # 0 = Real News, 1 = Fake News
            if influencer_type == 1:
                # A higher factor due to theory of misinformation
                agent_opinion = rd.randint(-100, -85)
                i_factor = rd.uniform(1, 2)
            else:
                agent_opinion = rd.randint(75, 100)
                i_factor = rd.uniform(1, 1.75)
                
            self.agents.append(InfluencerAgent(agent_id,agent_opinion,influencer_type,i_factor))
    
        # Initialize graph environment with agent nodes and edges
        self.graph_environment.add_nodes_from(make_agent_nodes(self.agents))
        self.graph_environment.add_weighted_edges_from(make_agents_connections(self.agents))
        
        # Record initial values of all agents before timesteps are executed
        self.record_data()
    
    def timestep(self):
        nodes_arr = list(self.graph_environment._node.keys())
        rd.shuffle(nodes_arr)
        for agent_id in nodes_arr:
            agent = self.graph_environment._node[agent_id]['agent']
            agent_network = list(self.graph_environment.neighbors(agent_id))
            # Execute influencing process from each individual node to its network
            agent.influence_agent(self.graph_environment,agent_network)
        
        # Record Data for every timestep
        self.record_data()
        
    def record_data(self):
        for agent in self.graph_environment._node.values():
            agent_obj = agent['agent']
            if isinstance(agent_obj,InfluencerAgent) == True:
                timestep_df = {'Timestep':f'T{self.timestep_val}',
                               'Agent Id':agent_obj.agent_id,
                               'Agent Type':'InfluencerAgent',
                               'Opinion':agent_obj.opinion,
                               'Influence Susceptibility':np.nan,
                               'Influence Factor':agent_obj.i_factor,
                               'Network':list(self.graph_environment.neighbors(agent_obj.agent_id))}
                self.dataset = self.dataset.append(timestep_df,ignore_index=True)
            elif isinstance(agent_obj,CommonerAgent) == True:
                timestep_df = {'Timestep':f'T{self.timestep_val}',
                               'Agent Id':agent_obj.agent_id,
                               'Agent Type':'CommonerAgent',
                               'Opinion':agent_obj.opinion,
                               'Influence Susceptibility':agent_obj.i_susceptibility,
                               'Influence Factor':np.nan,
                               'Network':list(self.graph_environment.neighbors(agent_obj.agent_id))}
                self.dataset = self.dataset.append(timestep_df,ignore_index=True)
        self.timestep_val += 1
        
    def end(self):
        raise Exception('Not yet implemented')

# =============================================================================
# Testing environment
# =============================================================================

# Benchmarking

# Performance depended on population and amount of timesteps
start = time.time()

timesteps = 50

model = Model(20,(75,25))
draw_graph_environment(model)

for i in range(timesteps):
    model.timestep()

display_df = model.dataset

done = time.time()
elapsed = done - start
print(f'Running Time: {elapsed}')