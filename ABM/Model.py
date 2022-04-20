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

class Model():
    
    def __init__(self,population, distribution, user_network, influencer_network, f_network_mult_factor, homophily_weight_range, f_influence_factor, r_influence_factor, f_opinion, r_opinion, susceptibility,group_opinion_limit_val,group_homophily_limit_val):
        
        # Initialize Agent list
        self.agents = []
        
        # Initialize population
        self.population = population
        
        # Initialize Graph
        self.graph_environment = nx.Graph()
        
        # Initialize Pd.DataFrame for data collection
        pd.set_option("expand_frame_repr", True)
        self.dataset_individual_agent = pd.DataFrame(columns=['Timestep','Agent_id','Agent Type','Opinion','Influence Susceptibility','Influence Factor','Network','Echo chamber'])
        self.dataset_global_opinion = pd.DataFrame(columns=['Timestep','Population','Global Opinion','Influencer Opinion Included'])
        self.dataset_groups = pd.DataFrame(columns=['Timestep','Group id','Agents in group','size','average opinion'])
        
        # Track individual opinion of agents
        self.individual_agent = []
        
        # Track groups
        self.groups_dataframes = []
        
        # Track global opinion
        self.global_opinion = []
        
        # Track groups
        self.unique_group_id = 0
        self.groups = {}
        
        # Parameters for make_group() method
        self.group_opinion_limit_val = group_opinion_limit_val
        self.group_homophily_limit_val  = group_homophily_limit_val
        
        # Keeping track of timesteps
        self.timestep_val = 0
        
        
        user_dist,r_influencer_dist, f_influencer_dist = distribution
        if user_dist + r_influencer_dist + f_influencer_dist != 100:
            raise Exception("Population distribution mismatch. Must be equal to 100")

        self.user_population = round(self.population*(user_dist/100)) # Divides population into users and Influencers
        self.f_influencer_population = round(self.population*(f_influencer_dist/100)) # Divides population into users and f_Influencers
        self.r_influencer_population = round(self.population*(r_influencer_dist/100)) # Divides population into users and r_Influencers

        # boundary for unique agent ids
        self.pop_init_boundary = self.user_population + self.f_influencer_population
        
        # Define user susceptibility min and max ranges
        sus_min, sus_max = susceptibility
        # Generate a list of user opinions based on normal distribution theory
        self.user_norm_dist_opinion = list(normalDistNP(self.user_population))
        
        # create user agents        
        for i in range(0,self.user_population):
            agent_id = i
            agent_opinion = self.user_norm_dist_opinion.pop()
            i_susceptibility = rd.uniform(sus_min, sus_max)

            self.agents.append(UserAgent(agent_id,agent_opinion,-1,i_susceptibility))

        # create fake news influencer agents
        f_min_val, f_max_val = f_influence_factor
        f_min_op, f_max_op = f_opinion
        for i in range(self.user_population,self.pop_init_boundary):
            agent_id = i
            influencer_type = 1 # 0 = Real News, 1 = Fake News
            agent_opinion = rd.randint(f_min_op, f_max_op)
            i_factor = rd.uniform(f_min_val, f_max_val)

            self.agents.append(InfluencerAgent(agent_id,agent_opinion,-1,influencer_type,i_factor))            
        
        # create real news influencer agents
        r_min_val, r_max_val = r_influence_factor
        r_min_op, r_max_op = r_opinion
        for i in range(self.pop_init_boundary,self.population):
            agent_id = i
            influencer_type = 0 # 0 = Real News, 1 = Fake News
            agent_opinion = rd.randint(r_min_op, r_max_op)
            i_factor = rd.uniform(r_min_val, r_max_val)
                
            self.agents.append(InfluencerAgent(agent_id,agent_opinion,-1,influencer_type,i_factor))
    
        # Initialize graph environment with agent nodes and edges
        self.graph_environment.add_nodes_from(make_agent_nodes(self.agents))
        
        # "make_agent_connections()" takes model parameter inputs 
        self.graph_environment.add_weighted_edges_from(make_agents_connections(self.agents, user_network, influencer_network, f_network_mult_factor, homophily_weight_range))
        
        # Record initial values of all agents before timesteps are executed
        self.record_data_individual_agent()
        
        # Record initial global opinion before timesteps are executed
        self.record_data_global_opinion()
    
    def timestep(self):
        """
        The following method loops overs all agents and initiatize their built in influencing method.
        Every single agent influence every single friend agent in their network.
        
        Moreover, echo chambers are initalized and potentially left for every timestep
        
        Global opinion is also measured in the following method
        
        Returns
        -------
        Nothing

        """
        
        self.timestep_val += 1  
        
        # individual agent - influence 
        nodes_arr = list(self.graph_environment._node.keys())
        rd.shuffle(nodes_arr)
        for agent_id in nodes_arr:
            agent = self.graph_environment._node[agent_id]['agent']
            agent_network = list(self.graph_environment.neighbors(agent_id))
            # Execute influencing process from each individual node to its network
            agent.influence_agent(self.graph_environment,agent_network)
            
            # Reflect on global opinion at a slower pace
            if self.timestep_val % 25 == 0 and isinstance(agent,UserAgent):
                former_global_opinion = self.global_opinion[self.timestep_val-1]['Global Opinion']
                agent.global_opinion_reflection(former_global_opinion)
            
        # Create/leave groups
        self.join_groups(nodes_arr)
        self.potentially_leave_group(nodes_arr)
        
        # Recalculate group average opinions and polarize towards average group opinion
        for group in self.groups.values():
            group.calc_avg_opinion()
            group.polarize_agents()
        
        # Record Data for every timestep
        self.record_data_individual_agent()
        
        # Record data groups
        self.record_data_groups()
        
        # Record data global opinion
        self.record_data_global_opinion()
    
    def join_groups(self,agent_list):
        """
        The following method will walk through each agent and potentially create an group/echo chamber
        if opinion and homophily are close enough.

        Parameters
        ----------
        agent_list : list of agent ids
            takes a list of agent ids as input

        Returns
        -------
        None.

        """
        
        for agent_id in agent_list:
            # Retrieve agent object
            agent = self.graph_environment._node[agent_id]['agent']
            # Retrieve agent object's friend list of ids
            agent_network = list(self.graph_environment.neighbors(agent_id))    
            
            for agent_friend_id in agent_network:
                # Retrieve a specific friend in friendlist
                agent_friend = self.graph_environment._node[agent_friend_id]['agent']
                
                if isinstance(agent,UserAgent) and isinstance(agent_friend,UserAgent) and agent_friend.group_id == -1:
                    # Calculate whether current agent and a specific friend have almost same opinion
                    similar_opinion_bool = True if abs(agent.opinion - agent_friend.opinion) < self.group_opinion_limit_val else False
                    # Check the homophily rate of the friendship
                    homophily_rate = self.graph_environment.get_edge_data(agent.agent_id,agent_friend.agent_id)['weight']
                    homophily_bool = True if homophily_rate > self.group_homophily_limit_val else False
                
                    if similar_opinion_bool and homophily_bool:
                        if agent.group_id == -1:
                            if agent.opinion < -50 or agent.opinion > 50:
                                # if current agent not in group. Create one and place them in it
                                group = Group(self.unique_group_id,agent.opinion)
                                group.join_group(agent)
                                group.join_group(agent_friend)
                                self.groups[f'{self.unique_group_id}'] = group
                                self.unique_group_id += 1
                        else:
                            # If current agent is in a group. Put the friend in it as well
                            group = self.groups[f'{agent.group_id}']
                            group.join_group(agent_friend)
                    
    def potentially_leave_group(self,agent_list):
        """
        The following method will walk through each agent and potentially make an agent leave
        an existing group if the agents opinion no longer reflects the average opinion of the group

        Parameters
        ----------
        agent_list : list of agent ids
            takes a list of agent ids as input

        Returns
        -------
        None.

        """
        
        for agent_id in agent_list:
            # Retrieve agent object
            agent = self.graph_environment._node[agent_id]['agent']
            
            if agent.group_id != -1:
                # Retrieve the group that the current agent are placed onto
                group = self.groups[f'{agent.group_id}']
                group_avg_opinion = group.avg_opinion
                group_opinion_disagreement = True if abs(agent.opinion-group_avg_opinion) > self.group_opinion_limit_val else False
                
                if group_opinion_disagreement or group.size == 1:
                    group.leave_group(agent)
        
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
                               'Agent_id':agent_obj.agent_id,
                               'Agent Type':'InfluencerAgent',
                               'Opinion':agent_obj.opinion,
                               'Influence Susceptibility':np.nan,
                               'Influence Factor':agent_obj.i_factor,
                               'Network':list(self.graph_environment.neighbors(agent_obj.agent_id)),
                               'Echo chamber':np.nan}
                self.individual_agent.append(timestep_df)
            elif isinstance(agent_obj,UserAgent) == True:
                timestep_df = {'Timestep':f'T{self.timestep_val}',
                               'Agent_id':agent_obj.agent_id,
                               'Agent Type':'UserAgent',
                               'Opinion':agent_obj.opinion,
                               'Influence Susceptibility':agent_obj.i_susceptibility,
                               'Influence Factor':np.nan,
                               'Network':list(self.graph_environment.neighbors(agent_obj.agent_id)),
                               'Echo chamber':agent_obj.group_id
                               }
                self.individual_agent.append(timestep_df)
        
    def record_data_groups(self):
        for group in self.groups.values():
            if group.size != 0:
                self.groups_dataframes.append({
                    'Timestep':f'T{self.timestep_val}',
                    'Group id': group.group_id,
                    'Agents in list': [x.agent_id for x in group.agent_list],
                    'Group size': group.size,
                    'Group average opinion': group.avg_opinion
                    })
        

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
            self.global_opinion.append({'Timestep':f'T{self.timestep_val}','Population':self.population,'Global Opinion':temp_global_opinion/self.user_population,'Influencer Opinion Included':'No'})

    def finalize_model(self):
        """
        A method to create pandas DataFrame of all the agents in the ABM.

        Returns
        -------
        None.

        """
        
        self.dataset_global_opinion = pd.DataFrame(self.global_opinion)
        self.dataset_individual_agent = pd.DataFrame(self.individual_agent)
        self.dataset_groups = pd.DataFrame(self.groups_dataframes)

# ============================================================================= #
#                            Testing environment                                #
# ============================================================================= #

if __name__ == '__main__':
    # Benchmarking
    start = time.time()
    
    ### Parameters ###
    params = {
        'timesteps': 500, # declare amount of timesteps
        "population": 300, # declare the overall population of the ABM
        "population_distribution":(25, 37.5, 37.5), # percentages: user, fake, real
        "user_network": 3, # how many connections should a typical user have
        "influencer_network": 2, # how many connections should a typical influencer have
        "finfluencer_network_mult_factor": 1, # starts at 1 - a multiplication of fake news influencer network - due to fake news spreading more
        "homophily_weight_range": 2, # homophily between users
        "f_influence_factor": (1, 2), # influence factor - fake news influencer (should be higher for Finfluencer)
        "r_influence_factor": (1, 2), # influence factor - real news influencer
        "f_opinion": (-100, -50), #  range of opinion - fake news influencer (should be more radical for Finfluencer)
        "r_opinion": (50, 100), # range of opinion - real news influencer
        "user_susceptibility": (1, 2), # susceptibility - user - random value between 1 and 2
        'echo_chamber_entrance_limit': 10, # determine the limit for when a opinion should reflect a potential join of an echo chamber
        'echo_chamber_homophily_limit': 1.6 # determine the homophily between agents that should be in an echo chamber
    }
    
    # Create model
    model = Model(params['population'], params['population_distribution'], params['user_network'], params['influencer_network'], params['finfluencer_network_mult_factor'], params['homophily_weight_range'], params['f_influence_factor'], params['r_influence_factor'], params['f_opinion'], params['r_opinion'], params['user_susceptibility'],params['echo_chamber_entrance_limit'],params['echo_chamber_homophily_limit'])
    
    # Used to draw the graph
    draw_graph_environment(model)
    
    # run sim (run timesteps)
    for i in range(params['timesteps']):
        model.timestep()
    
    # Create a pandas dataframe with the final global opinion values
    model.finalize_model()
    
    ### temp variables ###        
    # record data 
    df_individual_opinion = model.dataset_individual_agent
    df_groups = model.dataset_groups
    df_global_opinion = model.dataset_global_opinion
    
    groups = model.groups
    ######################
    
    done = time.time()
    elapsed = done - start
    print(f'Running Time: {elapsed}')