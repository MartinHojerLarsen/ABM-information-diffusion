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
        # Initialize Pd.DataFrame for data collection
        pd.set_option("expand_frame_repr", True)
        self.dataset_individual_agent = pd.DataFrame(columns=['Timestep','Agent Id','Agent Type','Opinion','Influence Susceptibility','Influence Factor','Network'])
        self.dataset_global_opinion = pd.DataFrame(columns=['Timestep','Population','Global Opinion','Influencer Opinion Included'])
        
        # Keeping track of timesteps
        self.timestep_val = 0
        
        commoner_dist,r_influencer_dist, f_influencer_dist = distribution
        if commoner_dist + r_influencer_dist + f_influencer_dist != 100:
            raise Exception("Population distribution mismatch. Must be equal to 100")

        self.commoner_population = round(self.population*(commoner_dist/100)) # Divides population into Commoners and Influencers
        self.f_influencer_population = round(self.population*(f_influencer_dist/100)) # Divides population into Commoners and Influencers
        self.r_influencer_population = round(self.population*(r_influencer_dist/100)) # Divides population into Commoners and Influencers

        # boundary for unique agent ids
        self.pop_init_boundary = self.commoner_population + self.f_influencer_population

        for i in range(0,self.commoner_population):
            # create commoner agents
            agent_id = i
            agent_opinion = rd.randint(-50, 50)
            i_susceptibility = rd.uniform(1, 2)

            self.agents.append(CommonerAgent(agent_id,agent_opinion,i_susceptibility))

        for i in range(self.commoner_population,self.pop_init_boundary):
            # create fake news influencer agents
            agent_id = i
            influencer_type = 1 # 0 = Real News, 1 = Fake News
            agent_opinion = rd.randint(-100, -85) # A bit higher due to theory of deeper influencing
            i_factor = rd.uniform(1, 2)

            self.agents.append(InfluencerAgent(agent_id,agent_opinion,influencer_type,i_factor))            

        for i in range(self.pop_init_boundary,self.population):
            # create real news influencer agents
            agent_id = i
            influencer_type = 0 # 0 = Real News, 1 = Fake News
            agent_opinion = rd.randint(80, 100)
            i_factor = rd.uniform(1, 1.75)
                
            self.agents.append(InfluencerAgent(agent_id,agent_opinion,influencer_type,i_factor))
    
        # Initialize graph environment with agent nodes and edges
        self.graph_environment.add_nodes_from(make_agent_nodes(self.agents))
        self.graph_environment.add_weighted_edges_from(make_agents_connections(self.agents))
        
        # Record initial values of all agents before timesteps are executed
        self.record_data_individual_agent()
    
    def timestep(self):
        """
        The following method loops overs all agents and initiatize their built in influencing method.
        Every single agent influence every single friend agent in their network.
        
        Returns
        -------
        Nothing

        """
        
        nodes_arr = list(self.graph_environment._node.keys())
        rd.shuffle(nodes_arr)
        for agent_id in nodes_arr:
            agent = self.graph_environment._node[agent_id]['agent']
            agent_network = list(self.graph_environment.neighbors(agent_id))
            # Execute influencing process from each individual node to its network
            agent.influence_agent(self.graph_environment,agent_network)
        
        # Record Data for every timestep
        self.record_data_individual_agent()
        
    def record_data_individual_agent(self):
        """
        This method fetches all data points for every agent during a single timestep.

        Returns
        -------
        Nothing

        """
        
        rows = []
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
                rows.append(timestep_df)
            elif isinstance(agent_obj,CommonerAgent) == True:
                timestep_df = {'Timestep':f'T{self.timestep_val}',
                               'Agent Id':agent_obj.agent_id,
                               'Agent Type':'CommonerAgent',
                               'Opinion':agent_obj.opinion,
                               'Influence Susceptibility':agent_obj.i_susceptibility,
                               'Influence Factor':np.nan,
                               'Network':list(self.graph_environment.neighbors(agent_obj.agent_id))}
                rows.append(timestep_df)
        self.dataset_individual_agent = self.dataset_individual_agent.append(rows,ignore_index=True)
        self.timestep_val += 1
        
    def record_data_collectives(self):
        raise Exception('Not yet implemented')

    def record_data_global_opinion(self,include_influencer_agent_op = False):
        """
        This method gathers the global opinion of all agents during every single timestep

        Parameters
        ----------
        include_influencer_agent_op : Boolean, optional
            Specify whether the opinion of influencer agent should be included in the dataset. The default is False.

        Returns
        -------
        Nothing

        """
        
        timesteps = self.dataset_individual_agent['Timestep'].unique()
        g_opinion_dict = []
        for tp in timesteps:
            if include_influencer_agent_op:
                g_opinion = self.dataset_individual_agent[self.dataset_individual_agent['Timestep'] == tp]
            else:
                g_opinion = self.dataset_individual_agent[(self.dataset_individual_agent['Timestep'] == tp) & (model.dataset_individual_agent['Agent Type'] == 'CommonerAgent')]
            # print(g_opinion['Opinion'].mean())
            g_opinion_average = g_opinion['Opinion'].mean()
            g_opinion_dict.append({'Timestep':tp,'Population':self.population,'Global Opinion':g_opinion_average,'Influencer Opinion Included':include_influencer_agent_op})
        self.dataset_global_opinion = self.dataset_global_opinion.append(g_opinion_dict,ignore_index=True)
# =============================================================================
# Testing environment
# =============================================================================

# Benchmarking
start = time.time()

# amount of timesteps
timesteps = 30

model = Model(75,(50,25,25))
draw_graph_environment(model)

for i in range(timesteps):
    model.timestep()

model.record_data_global_opinion()
df_individual_opinion = model.dataset_individual_agent
df_global_opinion = model.dataset_global_opinion

done = time.time()
elapsed = done - start
print(f'Running Time: {elapsed}')