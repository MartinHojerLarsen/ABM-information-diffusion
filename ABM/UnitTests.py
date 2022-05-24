#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:06:54 2022

@author: mmp
"""

import unittest
from Functions import *
from Group import *
from Model import *
from Agent import *

# Make various Unit Tests


# =============================================================================
# Model tests
# =============================================================================
class ModelTests(unittest.TestCase):
    
    def setup(self):
        # Do not change parameters since the UnitTests then will not work
        params = {
            'timesteps': 10, # declare amount of timesteps
            "population": 30, # declare the overall population of the ABM
            "distribution":(50, 25, 25), # percentages: commoner, fake, real
            "commoner_network": 3, # how many connections should a typical commoner have
            "influencer_network": 2, # how many connections should a typical influencer have
            "f_network_mult_factor": 1, # starts at 1 - a multiplication of fake news influencer network - due to fake news spreading more
            "homophily_weight_range": 2, # homophily between commoners
            "f_i_factor": (1, 2), # influence factor - fake news influencer (should be higher for Finfluencer)
            "r_i_factor": (1, 2), # influence factor - real news influencer
            "f_opinion": (-100, -50), #  range of opinion - fake news influencer (should be more radical for Finfluencer)
            "r_opinion": (50, 100), # range of opinion - real news influencer
            "susceptibility": (1, 2), # susceptibility - commoner - random value between 1 and 2
            'group_opinion_limit_val': 5, # determine the limit for when a opinion should reflect a potential join of an echo chamber
            'group_homophily_limit_val': 1.70 # determine the homophily between agents that should be in an echo chamber
        }

        model = Model(params['population'], params['distribution'], params['commoner_network'], params['influencer_network'], params['f_network_mult_factor'], params['homophily_weight_range'], params['f_i_factor'], params['r_i_factor'], params['f_opinion'], params['r_opinion'], params['susceptibility'],params['group_opinion_limit_val'],params['group_homophily_limit_val'])
        return model
    
    def test_model_initialization(self):
        model = self.setup()
        
        # Test amount of agents
        self.assertEqual(len(model.agents),30)
        # Test amount of agents in the graph environment
        self.assertEqual(len(model.graph_environment._node),30)
        
        # Test that UserAgents init values are not greater or less than 50 and -50
        for agent in model.agents:
            if isinstance(agent,UserAgent):
                self.assertLess(agent.opinion,50)
                self.assertGreater(agent.opinion,-50)
        
        # Test that InfluencerAgents init values are greater or less than 50 and -50
        for agent in model.agents: 
            if isinstance(agent,InfluencerAgent):
                if agent.agent_type == 1:
                    self.assertLessEqual(agent.opinion,-50)
                else:
                    self.assertGreaterEqual(agent.opinion,50)
    
    def test_model_join_group_1(self):
        model = self.setup()
        c1 = model.graph_environment._node[0]['agent']
        c1.opinion = 75 # For testing purpose
        c1_friends_id = list(model.graph_environment.neighbors(0))
        c1_friends_agents = []
        
        for agent_id in c1_friends_id:
            agent = model.graph_environment._node[agent_id]['agent']
            if isinstance(agent,UserAgent):
                
                """
                In this unit test we are testing both opinion and homophily between agents.
                
                """
                
                #Manipulated opinion for testing. Opinions are the same
                agent.opinion = c1.opinion
                #manipualted homophily for testing. Homophily is high
                model.graph_environment.get_edge_data(c1.agent_id,agent.agent_id)['weight'] = 2.0
                c1_friends_agents.append(agent)
        
        if len(c1_friends_agents) != 0:
            # Check that first agent is in group
            model.join_groups([c1.agent_id])
            
            # Check that Groups are not empty
            self.assertNotEqual(len(model.groups),0)
            
            # Check that first agent's group number is not -1
            self.assertNotEqual(c1.group_id,-1)
        
    def test_model_join_group_2(self):
        model = self.setup()
        c1 = model.graph_environment._node[0]['agent']
        c1.opinion = 75 # For testing purpose
        c1_friends_id = list(model.graph_environment.neighbors(0))
        c1_friends_agents = []
        
        for agent_id in c1_friends_id:
            agent = model.graph_environment._node[agent_id]['agent']
            """
            In this unit test we are testing that opinion are from each other and homophily is close between agents.
            
            """
            
            #Manipulated opinion for testing. Opinions are far from each other
            agent.opinion = 25
            #manipualted homophily for testing. Homophily is high
            model.graph_environment.get_edge_data(c1.agent_id,agent.agent_id)['weight'] = 2.0
            c1_friends_agents.append(agent)
        
        if len(c1_friends_agents) != 0:
            #Execute model join groups method
            model.join_groups([c1.agent_id])
            
            #Check that first agent is not in a group
            self.assertEqual(c1.group_id,-1)
        
    # def test_model_join_group_3(self):
    #     model = self.setup()
    #     c1 = model.graph_environment._node[0]['agent']
    #     c1.opinion = 75 # For testing purpose
    #     c1_friends_id = list(model.graph_environment.neighbors(0))
    #     c1_friends_agents = []
        
    #     for agent_id in c1_friends_id:
    #         agent = model.graph_environment._node[agent_id]['agent']
                
    #         """
    #         In this unit test we are testing that opinion close and homophily are far.
            
    #         """
            
    #         #Manipulated opinion for testing. Opinions are close to each other
    #         agent.opinion = c1.opinion
    #         #manipualted homophily for testing. Homophily is low
    #         model.graph_environment.get_edge_data(c1.agent_id,agent.agent_id)['weight'] = 1.1
    #         c1_friends_agents.append(agent)
        
    #     if len(c1_friends_agents) != 0:
    #         # Execute model join groups method
    #         model.join_groups([c1.agent_id])
            
    #         # Check that first agent's group id is -1 (representing as not being in a group)
    #         self.assertEqual(c1.group_id,-1)
        
    def test_model_join_group_4(self):
        model = self.setup()
        c1 = model.graph_environment._node[0]['agent']
        c1.opinion = 75 # For testing purpose
        c1_friends_id = list(model.graph_environment.neighbors(0))
        c1_friends_agents = []
        
        for agent_id in c1_friends_id:
            agent = model.graph_environment._node[agent_id]['agent']
                
            """
            In this unit test we are testing that opinions are far and homophilies are far.
            
            """
            
            #Manipulated opinion for testing. Opinions are far from each other
            agent.opinion = 25
            #manipualted homophily for testing. Homophily is low
            model.graph_environment.get_edge_data(c1.agent_id,agent.agent_id)['weight'] = 1.1
            c1_friends_agents.append(agent)
        
        if len(c1_friends_agents) != 0:
            # Execute model join groups method
            model.join_groups([c1.agent_id])
            
            # Check that first agent's group id is -1 (representing as not being in a group)
            self.assertEqual(c1.group_id,-1)
        
    def test_model_leave_group(self):
        # make a group
        model = self.setup()
        c1 = model.graph_environment._node[0]['agent']
        c1.opinion = 75 # For testing purpose
        c1_friends_id = list(model.graph_environment.neighbors(0))
        c1_friends_agents = []
        
        for agent_id in c1_friends_id:
            agent = model.graph_environment._node[agent_id]['agent']
            if isinstance(agent,UserAgent):
                
                """
                In this unit test we are testing both opinion and homophily between agents.
                
                """
                
                #Manipulated opinion for testing. Opinions are the same
                agent.opinion = c1.opinion
                #manipualted homophily for testing. Homophily is high
                model.graph_environment.get_edge_data(c1.agent_id,agent.agent_id)['weight'] = 2.0
                c1_friends_agents.append(agent)
        
        if len(c1_friends_agents) != 0:
            model.join_groups([c1.agent_id])
            
            self.assertNotEqual(c1.group_id,-1)
            
            model.potentially_leave_group([c1.agent_id])
            
            self.assertNotEqual(c1.group_id,-1)
            
            # Manipualte c1's opinion to something else than the rest of the group
            c1.opinion = -75
            
            model.potentially_leave_group([c1.agent_id])
            
            # Make sure that c1 has left the group
            self.assertEqual(c1.group_id,-1)
            
            # Make sure that c1 is not in the group
            agents_in_group = model.groups['0'].agent_list
            agents_in_group = list(map(lambda x: x.agent_id,agents_in_group))
            
            self.assertFalse(c1.agent_id in agents_in_group)
    
# =============================================================================
# Agent tests
# =============================================================================
class AgentTests(unittest.TestCase):
    
    def setup(self): 
        # Do not change parameters since the UnitTests will not work then
        params = {
            'timesteps': 10, # declare amount of timesteps
            "population": 30, # declare the overall population of the ABM
            "distribution":(50, 25, 25), # percentages: commoner, fake, real
            "commoner_network": 3, # how many connections should a typical commoner have
            "influencer_network": 2, # how many connections should a typical influencer have
            "f_network_mult_factor": 1, # starts at 1 - a multiplication of fake news influencer network - due to fake news spreading more
            "homophily_weight_range": 2, # homophily between commoners
            "f_i_factor": (1, 2), # influence factor - fake news influencer (should be higher for Finfluencer)
            "r_i_factor": (1, 2), # influence factor - real news influencer
            "f_opinion": (-100, -50), #  range of opinion - fake news influencer (should be more radical for Finfluencer)
            "r_opinion": (50, 100), # range of opinion - real news influencer
            "susceptibility": (1, 2), # susceptibility - commoner - random value between 1 and 2
            'group_opinion_limit_val': 5, # determine the limit for when a opinion should reflect a potential join of an echo chamber
            'group_homophily_limit_val': 1.70 # determine the homophily between agents that should be in an echo chamber
        }

        model = Model(params['population'], params['distribution'], params['commoner_network'], params['influencer_network'], params['f_network_mult_factor'], params['homophily_weight_range'], params['f_i_factor'], params['r_i_factor'], params['f_opinion'], params['r_opinion'], params['susceptibility'],params['group_opinion_limit_val'],params['group_homophily_limit_val'])
        return model
        
    def test_commoner_influence_positive(self):
        model = self.setup()
        c1 = model.graph_environment._node[0]['agent']
        c1.opinion = 90
        network_ids = list(model.graph_environment.neighbors(0))
        
        list_of_neighbors = []
        
        for agent_id in network_ids:
            agent = model.graph_environment._node[agent_id]['agent']
            list_of_neighbors.append(agent)
        
        filtered_agents = [x for x in list_of_neighbors if isinstance(x,UserAgent)]
        filtered_agents_id = [x.agent_id for x in filtered_agents]
                
        if len(filtered_agents) == 0:
            self.test_commoner_influence_positive()
        
        agents_old_values = [(x.agent_id,round(x.opinion,5),x.i_susceptibility) for x in filtered_agents]
        
        # Execute influence method
        c1.influence_agent(model.graph_environment,filtered_agents_id)
        
        agents_new_values = [(x.agent_id,round(x.opinion,5),x.i_susceptibility) for x in filtered_agents]
        
        for index,old_agent_opinion in enumerate(agents_old_values):
            _,old_agent_opinion,_ = old_agent_opinion
            _,new_agent_opinion,_ = agents_new_values[index]
            
            c1_old_varians = abs(c1.opinion-old_agent_opinion)
            c1_new_varians = abs(c1.opinion-new_agent_opinion)
            
            self.assertLess(c1_new_varians,c1_old_varians)
    
    def test_commoner_influence_negative(self):
        model = self.setup()
        c1 = model.graph_environment._node[0]['agent']
        c1.opinion = -90
        network_ids = list(model.graph_environment.neighbors(0))
        
        list_of_neighbors = []
        
        for agent_id in network_ids:
            agent = model.graph_environment._node[agent_id]['agent']
            list_of_neighbors.append(agent)
        
        filtered_agents = [x for x in list_of_neighbors if isinstance(x,UserAgent)]
        filtered_agents_id = [x.agent_id for x in filtered_agents]
                
        if len(filtered_agents) == 0:
            self.test_commoner_influence_negative()
        
        agents_old_values = [(x.agent_id,round(x.opinion,5),x.i_susceptibility) for x in filtered_agents]
        
        # Execute influence method
        c1.influence_agent(model.graph_environment,filtered_agents_id)
        
        agents_new_values = [(x.agent_id,round(x.opinion,5),x.i_susceptibility) for x in filtered_agents]
        
        for index,old_agent_opinion in enumerate(agents_old_values):
            _,old_agent_opinion,_ = old_agent_opinion
            _,new_agent_opinion,_ = agents_new_values[index]
            
            c1_old_varians = abs(c1.opinion-old_agent_opinion)
            c1_new_varians = abs(c1.opinion-new_agent_opinion)
            
            self.assertLess(c1_new_varians,c1_old_varians)
        
    
    def test_influencer_influence_positive(self):
        model = self.setup()
        i1 = model.graph_environment._node[25]['agent']
        i1.opinion = 90
        network_ids = list(model.graph_environment.neighbors(25))
        
        list_of_neighbors = []
        
        for agent_id in network_ids:
            agent = model.graph_environment._node[agent_id]['agent']
            list_of_neighbors.append(agent)
        
        agents_old_values = [(x.agent_id,round(x.opinion,5),x.i_susceptibility) for x in list_of_neighbors]
        
        # Execute influence method
        i1.influence_agent(model.graph_environment,network_ids)
        
        agents_new_values = [(x.agent_id,round(x.opinion,5),x.i_susceptibility) for x in list_of_neighbors]
        
        for index,old_agent_opinion in enumerate(agents_old_values):
            _,old_agent_opinion,_ = old_agent_opinion
            _,new_agent_opinion,_ = agents_new_values[index]
            
            i1_old_varians = abs(i1.opinion-old_agent_opinion)
            i1_new_varians = abs(i1.opinion-new_agent_opinion)
            
            self.assertLess(i1_new_varians,i1_old_varians)
    
    def test_influencer_influence_negative(self):
        model = self.setup()
        i1 = model.graph_environment._node[25]['agent']
        i1.opinion = -90
        network_ids = list(model.graph_environment.neighbors(25))
        
        list_of_neighbors = []
        
        for agent_id in network_ids:
            agent = model.graph_environment._node[agent_id]['agent']
            list_of_neighbors.append(agent)
        
        agents_old_values = [(x.agent_id,round(x.opinion,5),x.i_susceptibility) for x in list_of_neighbors]
        
        # Execute influence method
        i1.influence_agent(model.graph_environment,network_ids)
        
        agents_new_values = [(x.agent_id,round(x.opinion,5),x.i_susceptibility) for x in list_of_neighbors]
        
        for index,old_agent_opinion in enumerate(agents_old_values):
            _,old_agent_opinion,_ = old_agent_opinion
            _,new_agent_opinion,_ = agents_new_values[index]
            
            i1_old_varians = abs(i1.opinion-old_agent_opinion)
            i1_new_varians = abs(i1.opinion-new_agent_opinion)
            
            self.assertLess(i1_new_varians,i1_old_varians)
            
    def test_influencer_influence_factor(self):
        model = self.setup()
        
        # influence agent 1
        i1 = model.graph_environment._node[25]['agent']
        i1.opinion = -90
        i1.i_factor = 1.3
        i1_network = list(model.graph_environment.neighbors(25))
        
        # UserAgent 1
        # Check that influencerAgent has a network
        if len(i1_network) != 0:
            c1 = model.graph_environment._node[i1_network[0]]['agent']
            c1.opinion = 50
            c1.i_susceptibility = 1.5

        # influence agent 2
        i2 = model.graph_environment._node[26]['agent']
        i2.opinion = -90
        i2.i_factor = 1.6
        i2_network = list(model.graph_environment.neighbors(26))
        
        # UserAgent 2
        # Check that influencerAgent has a network
        if len(i2_network) != 0:
            c2 = model.graph_environment._node[i2_network[0]]['agent']
            c2.opinion = 50
            c2.i_susceptibility = 1.5
            
        i1.influence_agent(model.graph_environment,[i1_network[0]])
        i2.influence_agent(model.graph_environment,[i2_network[0]])
        
        if len(i1_network) != 0 and len(i2_network) != 0:
            if c1.agent_id != c2.agent_id:
                self.assertLess(c2.opinion, c1.opinion)
            
    def test_global_opinion_reflection_positive(self):
        fake_global_opinion = 5
        c1 = UserAgent(0,25,-1,1.3)
        c2 = UserAgent(1,-25,-1,1.3)
        
        c1_opinion_old = c1.opinion
        c2_opinion_old = c2.opinion
        
        # Reflect on global opinion
        c1.global_opinion_reflection(fake_global_opinion)
        c2.global_opinion_reflection(fake_global_opinion)
        
        self.assertNotEqual(c1.opinion,c1_opinion_old)
        self.assertNotEqual(c2.opinion,c2_opinion_old)
        self.assertLess(c1.opinion,c1_opinion_old)
        self.assertGreater(c2.opinion,c2_opinion_old)
        
        # Reflect on global opinion again
        c1.global_opinion_reflection(fake_global_opinion)
        c2.global_opinion_reflection(fake_global_opinion)
        
        self.assertLess(c1.opinion,c1_opinion_old)
        self.assertGreater(c2.opinion,c2_opinion_old)
        
    def test_global_opinion_reflection_positive2(self):
        fake_global_opinion = 50
        c1 = UserAgent(0,25,-1,1.3)
        c2 = UserAgent(1,-25,-1,1.3)
        
        c1_opinion_old = c1.opinion
        c2_opinion_old = c2.opinion
        
        # Reflect on global opinion
        c1.global_opinion_reflection(fake_global_opinion)
        c2.global_opinion_reflection(fake_global_opinion)
        
        self.assertNotEqual(c1.opinion,c1_opinion_old)
        self.assertNotEqual(c2.opinion,c2_opinion_old)
        self.assertGreater(c1.opinion,c1_opinion_old)
        # assertLess because the difference is so high that it has opposite effect
        self.assertLess(c2.opinion,c2_opinion_old)
        
        # Reflect on global opinion again
        c1.global_opinion_reflection(fake_global_opinion)
        c2.global_opinion_reflection(fake_global_opinion)
        
        self.assertGreater(c1.opinion,c1_opinion_old)
        self.assertLess(c2.opinion,c2_opinion_old)
        
        
    def test_global_opinion_reflection_negative(self):
        fake_global_opinion = -5
        c1 = UserAgent(0,25,-1,1.3)
        c2 = UserAgent(1,-25,-1,1.3)
        
        c1_opinion_old = c1.opinion
        c2_opinion_old = c2.opinion
        
        # Reflect on global opinion
        c1.global_opinion_reflection(fake_global_opinion)
        c2.global_opinion_reflection(fake_global_opinion)
        self.assertNotEqual(c1.opinion,c1_opinion_old)
        self.assertNotEqual(c2.opinion,c2_opinion_old)
        self.assertLess(c1.opinion,c1_opinion_old)
        self.assertGreater(c2.opinion,c2_opinion_old)
        
        # Reflect on global opinion again
        c1.global_opinion_reflection(fake_global_opinion)
        c2.global_opinion_reflection(fake_global_opinion)
        
        self.assertLess(c1.opinion,c1_opinion_old)
        self.assertGreater(c2.opinion,c2_opinion_old)
        
    def test_global_opinion_reflection_negative2(self):
        fake_global_opinion = -50
        c1 = UserAgent(0,25,-1,1.3)
        c2 = UserAgent(1,-25,-1,1.3)
        
        c1_opinion_old = c1.opinion
        c2_opinion_old = c2.opinion
        
        # Reflect on global opinion
        c1.global_opinion_reflection(fake_global_opinion)
        c2.global_opinion_reflection(fake_global_opinion)
        self.assertNotEqual(c1.opinion,c1_opinion_old)
        self.assertNotEqual(c2.opinion,c2_opinion_old)
        self.assertGreater(c1.opinion,c1_opinion_old)
        self.assertLess(c2.opinion,c2_opinion_old)
        
        # Reflect on global opinion again
        c1.global_opinion_reflection(fake_global_opinion)
        c2.global_opinion_reflection(fake_global_opinion)
        
        self.assertGreater(c1.opinion,c1_opinion_old)
        self.assertLess(c2.opinion,c2_opinion_old)
        
        
    def test_global_opinion_reflection_negative3(self):
        fake_global_opinion = -24
        c1 = UserAgent(0,25,-1,1.3)
        c2 = UserAgent(1,-25,-1,1.3)
        
        c1_opinion_old = c1.opinion
        c2_opinion_old = c2.opinion
        
        # Reflect on global opinion
        c1.global_opinion_reflection(fake_global_opinion)
        c2.global_opinion_reflection(fake_global_opinion)
        self.assertNotEqual(c1.opinion,c1_opinion_old)
        self.assertNotEqual(c2.opinion,c2_opinion_old)
        self.assertLess(c1.opinion,c1_opinion_old)
        self.assertGreater(c2.opinion,c2_opinion_old)
        
        # Reflect on global opinion again
        c1.global_opinion_reflection(fake_global_opinion)
        c2.global_opinion_reflection(fake_global_opinion)
        
        self.assertLess(c1.opinion,c1_opinion_old)
        self.assertGreater(c2.opinion,c2_opinion_old)
        
# =============================================================================
# Group tests
# =============================================================================
class GroupTests(unittest.TestCase):
    
    def test_make_group(self):
        grp = Group(1,75)
        
        self.assertIsInstance(grp, Group)
        self.assertEqual(grp.size, 0)
                
    def test_add_to_group(self):
        grp = Group(2,-75)
        c1 = UserAgent(1, 50, -1, 1.2)
        c2 = UserAgent(2, 21, -1, 1.4)
        
        grp.join_group(c1)
        grp.join_group(c2)
        
        self.assertEqual(grp.size, 2)
        
    def test_leave_group(self):
        grp = Group(2,-75)
        c1 = UserAgent(1, 50, -1, 1.2)
        c2 = UserAgent(2, 21, -1, 1.4)
        
        grp.join_group(c1)
        grp.join_group(c2)
        
        self.assertEqual(grp.size, 2)
        
        grp.leave_group(c1)
        
        self.assertNotEqual(grp.size, 2)
        
        grp.leave_group(c2)
        
        self.assertEqual(grp.size, 0)
        
    def test_calculate_avg_opinion(self):
        grp = Group(2,75)
        c1 = UserAgent(1, 75, -1, 1.2)
        c2 = UserAgent(2, 100, -1, 1.4)
        c3 = UserAgent(3, 80, -1, 1.4)
        grp.join_group(c1)
        grp.join_group(c2)
        
        group_avg_opinion = (c1.opinion+c2.opinion)/2
        self.assertEqual(grp.avg_opinion, group_avg_opinion)
        
        group_avg_opinion_2 = (c1.opinion+c2.opinion+c3.opinion)/3
        grp.join_group(c3)
        
        self.assertEqual(grp.avg_opinion, group_avg_opinion_2)
        
        grp.leave_group(c3)
        
        self.assertEqual(grp.avg_opinion, group_avg_opinion)
    
    def test_echo_chamber_limit_value(self):
        # this functionality is basically being mainted by the group class
        
        grp = Group(2,-75) # init value
        c1 = UserAgent(1, -80, -1, 1.2)
        c2 = UserAgent(2, -90, -1, 1.4)
        c3 = UserAgent(2, 17, -1, 1.4)
        grp.join_group(c1)
        grp.join_group(c2)
        
        self.assertEqual(grp.avg_opinion, -85)
        
        grp.join_group(c3)
        
        self.assertNotEqual(grp.avg_opinion, -51.0)
        
        # Since average cannot go below initalization value
        self.assertEqual(grp.avg_opinion, -75)        
       
    def test_polarize_positive(self):
       c1 = UserAgent(0, 80, -1, 50)
       c2 = UserAgent(1, 90, -1, 60)
        
       grp = Group(1,70)
        
       grp.join_group(c1)
       grp.join_group(c2)
        
       self.assertEqual(grp.avg_opinion,85)
        
       grp.polarize_agents()
       
       self.assertEqual(c1.opinion,85)
       self.assertEqual(c2.opinion,87.5)
       
    def test_polarize_negative(self):
       c1 = UserAgent(0, -80, -1, 50)
       c2 = UserAgent(1, -90, -1, 60)
       
       grp = Group(1,-70)
        
       grp.join_group(c1)
       grp.join_group(c2)
        
       self.assertEqual(grp.avg_opinion,-85)
        
       grp.polarize_agents()
       
       self.assertEqual(c1.opinion,-85)
       self.assertEqual(c2.opinion,-87.5)



# =============================================================================
# Function tests
# =============================================================================

class FunctionsTests(unittest.TestCase):
    
    def test_normalDistNP(self):
        arr = []
        sum_arr = 0
        for i in range(30):
            arr.append(normalDistNP(30))
        
        for j in arr:
            sum_arr += len(j)
        
        self.assertEqual(sum_arr,900)
        
    def test_make_agent_nodes(self):
        c1 = UserAgent(1, -80, -1, 1.2)
        c2 = UserAgent(2, -90, -1, 1.4)
        c3 = UserAgent(2, 17, -1, 1.4)
        
        agent_list = [c1,c2,c3]
        
        self.assertEqual(agent_list[0].opinion, -80)
        self.assertEqual(agent_list[1].opinion, -90)
        self.assertNotEqual(agent_list[2].opinion, -80)
        
        nodes = make_agent_nodes(agent_list)
        
        for row in nodes:
            self.assertTrue(row[0] == row[1]['agent'].agent_id)
    
    def test_make_agents_connections(self):
        c1 = UserAgent(0, -80, -1, 1.2)
        c2 = UserAgent(1, -90, -1, 1.4)
        c3 = UserAgent(2, 17, -1, 1.4)
        i1 = InfluencerAgent(3, -80, -1, 1, 1.7)
        i2 = InfluencerAgent(4, 80, -1, 0, 1.82)
        
        nodes = [c1,c2,c3,i1,i2]
        edges = make_agents_connections(nodes, 5, 7, 1, 1.6)
        
        for edge in edges:
            a1,a2,w = edge
            if isinstance(a1, UserAgent) and isinstance(a2, UserAgent):
                self.assertNotEqual(w, 0)
            elif isinstance(a1, InfluencerAgent) and isinstance(a2, UserAgent):
                self.assertEqual(w, 0)
        


if __name__ == '__main__':
    unittest.main()
