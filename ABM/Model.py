# Import statements
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm
from re import I
from Agent import *
from Group import *
import random as rd
from Functions import *
import pandas as pd
import numpy as np
import time
#from Post import *

class Model():
    
    def __init__(self,population, distribution, commoner_network, influencer_network, f_network_mult_factor, homophily_weight_range, f_i_factor, r_i_factor, f_opinion, r_opinion, susceptibility):
        
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
        
        # Track individual opinion of agents
        self.individual_agent = [] 
        
        # Track global opinion
        self.global_opinion = []
        
        # Groups list of dictionary
        self.groups = [] # not being used at the moment
        
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
        
        # Define commoner susceptibility min and max ranges
        sus_min, sus_max = susceptibility
        # Generate a list of commoner opinions based on normal distribution theory
        self.commoner_norm_dist_opinion = list(normalDistNP(self.commoner_population))
        
        for i in range(0,self.commoner_population):
            # create commoner agents
            agent_id = i
            agent_opinion = self.commoner_norm_dist_opinion.pop()
            i_susceptibility = rd.uniform(sus_min, sus_max)

            self.agents.append(CommonerAgent(agent_id,agent_opinion,-1,i_susceptibility))

        f_min_val, f_max_val = f_i_factor
        f_min_op, f_max_op = f_opinion
        for i in range(self.commoner_population,self.pop_init_boundary):
            # create fake news influencer agents
            agent_id = i
            influencer_type = 1 # 0 = Real News, 1 = Fake News
            agent_opinion = rd.randint(f_min_op, f_max_op)
            i_factor = rd.uniform(f_min_val, f_max_val)

            self.agents.append(InfluencerAgent(agent_id,agent_opinion,-1,influencer_type,i_factor))            

        r_min_val, r_max_val = r_i_factor
        r_min_op, r_max_op = r_opinion
        for i in range(self.pop_init_boundary,self.population):
            # create real news influencer agents
            agent_id = i
            influencer_type = 0 # 0 = Real News, 1 = Fake News
            agent_opinion = rd.randint(r_min_op, r_max_op)
            i_factor = rd.uniform(r_min_val, r_max_val)
                
            self.agents.append(InfluencerAgent(agent_id,agent_opinion,-1,influencer_type,i_factor))
    
        
        # Initialize groups - 10 value increments for now
        #   so it will be: g1 = -100 to -90, g2 = -90 to -80 etc. 
        #   opinion values for groups:
        # group_start_value = -100
        # group_end_value = -90
        # for i in range(20):
        #     self.groups[i] = Group(i, group_start_value, group_end_value)
        #     group_start_value += 10
        #     group_end_value += 10
    
    
        # Initialize graph environment with agent nodes and edges
        self.graph_environment.add_nodes_from(make_agent_nodes(self.agents))
        # "make_agent_connections()" takes model parameter inputs 
        self.graph_environment.add_weighted_edges_from(make_agents_connections(self.agents, commoner_network, influencer_network, f_network_mult_factor, homophily_weight_range))
        
        # Record initial values of all agents before timesteps are executed
        self.record_data_individual_agent()
        
        # Record initial global opinion before timesteps are executed
        self.record_data_global_opinion()
    
    def timestep(self):
        """
        The following method loops overs all agents and initiatize their built in influencing method.
        Every single agent influence every single friend agent in their network.
        
        Returns
        -------
        Nothing

        """
        
        # individual agent - influence 
        nodes_arr = list(self.graph_environment._node.keys())
        rd.shuffle(nodes_arr)
        for agent_id in nodes_arr:
            agent = self.graph_environment._node[agent_id]['agent']
            agent_network = list(self.graph_environment.neighbors(agent_id))
            # Execute influencing process from each individual node to its network
            agent.influence_agent(self.graph_environment,agent_network)
        
        
            # =============================================================================
            #         NÅET HERTIL 
            # =============================================================================
            # Every 25th timestep - check group_opinion and join group
            # checking global group list - if true join group 
            # if agent.check_opinion(self.groups):
                # join the group
            # else:
                #continue
        
        # Record Data for every timestep
        self.record_data_individual_agent()
        
        #record data global
        self.record_data_global_opinion()
        
    def record_data_individual_agent(self):
        """
        This method fetches all data points for every agent during a single timestep.

        Returns
        -------
        Nothing

        """
        
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
                self.individual_agent.append(timestep_df)
            elif isinstance(agent_obj,CommonerAgent) == True:
                timestep_df = {'Timestep':f'T{self.timestep_val}',
                               'Agent Id':agent_obj.agent_id,
                               'Agent Type':'CommonerAgent',
                               'Opinion':agent_obj.opinion,
                               'Influence Susceptibility':agent_obj.i_susceptibility,
                               'Influence Factor':np.nan,
                               'Network':list(self.graph_environment.neighbors(agent_obj.agent_id))}
                self.individual_agent.append(timestep_df)
        self.timestep_val += 1
        
    def record_data_collectives(self):
        raise Exception("not yet implemented")
 
        

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
        nodes_arr = list(self.graph_environment._node.keys())
        temp_global_opinion = 0
        for agent_id in nodes_arr:
            agent = self.graph_environment._node[agent_id]['agent']
            
            if isinstance(agent,InfluencerAgent) == True and include_influencer_agent_op == False:
                continue
            
            temp_global_opinion += agent.opinion
            
        if include_influencer_agent_op:
            self.global_opinion.append({'Timestep':f'T{self.timestep_val}','Population':self.population,'Global Opinion':temp_global_opinion/self.population,'Influencer Opinion Included':'Yes'})
        else:
            self.global_opinion.append({'Timestep':f'T{self.timestep_val}','Population':self.population,'Global Opinion':temp_global_opinion/self.commoner_population,'Influencer Opinion Included':'No'})

    def finalize_model(self):
        self.dataset_global_opinion = pd.DataFrame(self.global_opinion)
        self.dataset_individual_agent = pd.DataFrame(self.individual_agent)

# ============================================================================= #
#                            Testing environment                                #
# ============================================================================= #

# Benchmarking
start = time.time()

# amount of timesteps
timesteps = 3

### Varaibles ###

params = {
    "population": 4,
    "distribution":(50, 25, 25), # percentages: commoner, fake, real
    "commoner_network": 3,
    "influencer_network": 2,
    "f_network_mult_factor": 1.5, # starts at 1 - a multiplication of influencer network - due to fake news spreading more
    "homophily_weight_range": 1.3, # homophily between commoners
    "f_i_factor": (1.5, 2), # influence factor - fake news influencer
    "r_i_factor": (1, 2), # influence factor - real news influencer
    "f_opinion": (-100, -80), #  range of opinion - fake news influencer
    "r_opinion": (50, 100), # range of opinion - real news influencer
    "susceptibility": (1, 2) # susceptibility - commoner - random value between 1 and 2
}


# create model


##############
model = Model(params['population'], params['distribution'], params['commoner_network'], params['influencer_network'], params['f_network_mult_factor'], params['homophily_weight_range'], params['f_i_factor'], params['r_i_factor'], params['f_opinion'], params['r_opinion'], params['susceptibility'])
draw_graph_environment(model)

# run sim (run timesteps)
for i in range(timesteps):
    model.timestep()

# Create a pandas dataframe with the final global opinion values
model.finalize_model()

##############

        
# record data 
df_individual_opinion = model.dataset_individual_agent
df_global_opinion = model.dataset_global_opinion

# To JSON format
# df_json = df_individual_opinion.to_json()

done = time.time()
elapsed = done - start

#### TEST ####
# c1 = model.graph_environment._node[0]["agent"]

# c2 = model.graph_environment._node[1]["agent"]

# c3 = model.graph_environment._node[2]["agent"]

# print(c1.check_homophily(c2, model.graph_environment))

print(f'Running Time: {elapsed}')