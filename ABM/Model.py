# Model dependencies
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
import openpyxl
####################

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
        self.dataset_individual_agent = pd.DataFrame()
        self.dataset_global_opinion = pd.DataFrame()
        self.dataset_groups = pd.DataFrame()
        
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
        
        # Create user agents        
        for i in range(0,self.user_population):
            agent_id = i
            agent_opinion = self.user_norm_dist_opinion.pop()
            i_susceptibility = rd.uniform(sus_min, sus_max)

            self.agents.append(UserAgent(agent_id,agent_opinion,-1,i_susceptibility))

        # Create fake news influencer agents
        f_min_val, f_max_val = f_influence_factor
        f_min_op, f_max_op = f_opinion
        for i in range(self.user_population,self.pop_init_boundary):
            agent_id = i
            influencer_type = 1 # 0 = Real News, 1 = Fake News
            agent_opinion = rd.randint(f_min_op, f_max_op)
            i_factor = rd.uniform(f_min_val, f_max_val)

            self.agents.append(InfluencerAgent(agent_id,agent_opinion,-1,influencer_type,i_factor))            
        
        # Create real news influencer agents
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
        
        Moreover, echo chambers are initalized and potentially joiend/left for every timestep
        
        Global opinion is also measured in the following method
        
        All behavior/interaction for agents, groups and global opinion are recorded for every timestep.
        
        Returns
        -------
        Nothing

        """
        
        self.timestep_val += 1  
        
        # Individual agent - influence 
        nodes_arr = list(self.graph_environment._node.keys())
        rd.shuffle(nodes_arr)
        for agent_id in nodes_arr:
            agent = self.graph_environment._node[agent_id]['agent']
            agent_network = list(self.graph_environment.neighbors(agent_id))
            # Execute influencing process from each individual node to its network
            agent.influence_agent(self.graph_environment,agent_network)
            
            # # Reflect on global opinion at a slower pace
            if self.timestep_val % 25 == 0 and isinstance(agent,UserAgent):
                former_global_opinion = self.global_opinion[self.timestep_val-1]['global_opinion']
                agent.global_opinion_reflection(former_global_opinion)
        
        # Create/leave groups
        self.join_groups(nodes_arr)
        self.potentially_leave_group(nodes_arr)
        
        # Recalculate group average opinions and polarize towards average group opinion

        for group in self.groups.values():
            group.calc_avg_opinion()
            if self.timestep_val % 10 == 0:
                group.polarize_agents()
        
        # Record Data for every timestep
        if self.timestep_val % 10 == 0:
            self.record_data_individual_agent()
        
        # Record data groups
        self.record_data_groups()
        
        # Record data global opinion
        self.record_data_global_opinion()
        
    def join_groups(self,agent_list):
        """
        The following method will walk through each agent and potentially create an group/echo chamber
        if opinion and homophily are close enough.
        
        If a group already exists, the method will let friends of a given agent join the same echo chamber.

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
                
                if agent_friend.group_id == -1:
                    # Calculate whether current agent and a specific friend have almost same opinion
                    similar_opinion_bool = True if abs(agent.opinion - agent_friend.opinion) < self.group_opinion_limit_val else False
                    
                    # Check the homophily rate of the friendship
                    homophily_rate = self.graph_environment.get_edge_data(agent.agent_id,agent_friend.agent_id)['weight']
                    homophily_bool = True if homophily_rate > self.group_homophily_limit_val else False
                
                    if isinstance(agent,UserAgent) and isinstance(agent_friend,UserAgent) and similar_opinion_bool and homophily_bool:
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
                            
                    elif ((isinstance(agent,InfluencerAgent) and isinstance(agent_friend,UserAgent)) or (isinstance(agent,UserAgent)) and isinstance(agent_friend,InfluencerAgent)) and similar_opinion_bool:
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
            network = list(self.graph_environment.neighbors(agent_obj.agent_id))
            network_influencers = [x for x in network if isinstance(self.graph_environment._node[x]['agent'],InfluencerAgent)]
            network_users = [x for x in network if isinstance(self.graph_environment._node[x]['agent'],UserAgent)]
            
            if isinstance(agent_obj,InfluencerAgent):
                timestep_df = {'timestep':self.timestep_val,
                               'agent_id':agent_obj.agent_id,
                               'agent_type':'I',
                               'opinion':agent_obj.opinion,
                               'influence_susceptibility':np.nan,
                               'influence_factor':agent_obj.i_factor,
                               'network_influencersAgents':len(network_influencers),
                               'network_userAgents':len(network_users),
                               'network_total':len(network_influencers) + len(network_users),
                               'echo_chamber':agent_obj.group_id}
                self.individual_agent.append(timestep_df)
            elif isinstance(agent_obj,UserAgent):
                timestep_df = {'timestep':self.timestep_val,
                               'agent_id':agent_obj.agent_id,
                               'agent_type':'U',
                               'opinion':agent_obj.opinion,
                               'influence_susceptibility':agent_obj.i_susceptibility,
                               'influence_factor':np.nan,
                               'network_influencersAgents':len(network_influencers),
                               'network_userAgents':len(network_users),
                               'network_total':len(network_influencers) + len(network_users),
                               'echo_chamber':agent_obj.group_id
                               }
                self.individual_agent.append(timestep_df)
        
    def record_data_groups(self):
        """
        This methods gathers all the information related to emerhed echo chambers/groups during a single timestep.

        Returns
        -------
        None.

        """
        for group in self.groups.values():
            if group.size != 0:
                self.groups_dataframes.append({
                    'timestep':self.timestep_val,
                    'group_id': group.group_id,
                    'agent_ids': [x.agent_id for x in group.agent_list],
                    'group_size': group.size,
                    'group_average_opinion': group.avg_opinion,
                    'group_limit_value': group.limit_value
                    })
        
    def record_data_global_opinion(self,include_influencer_agent_op = False):
        """
        This method gathers the global opinion of all agents during a single timestep.

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
            
            if isinstance(agent,InfluencerAgent) and include_influencer_agent_op == False:
                continue
            
            temp_global_opinion += agent.opinion
            
        if include_influencer_agent_op:
            self.global_opinion.append({'timestep':self.timestep_val,'population':self.population,'global_opinion':temp_global_opinion/self.population,'influencer_opinion_included':'Yes'})
        else:
            self.global_opinion.append({'timestep':self.timestep_val,'population':self.population,'global_opinion':temp_global_opinion/self.user_population,'influencer_opinion_included':'No'})

    def finalize_model(self):
        """
        The method gathers all the information for all the timesteps and inserts it into a pandas DataFrame.
        Returns
        -------
        None.

        """
        
        self.dataset_global_opinion = pd.DataFrame(self.global_opinion)
        self.dataset_individual_agent = pd.DataFrame(self.individual_agent)
        self.dataset_groups = pd.DataFrame(self.groups_dataframes)