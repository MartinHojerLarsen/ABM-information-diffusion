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



# Make various Unit Tests

class ModelTests(unittest.TestCase):
    
    def setup_model(self):
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

        self.model = Model(params['population'], params['distribution'], params['commoner_network'], params['influencer_network'], params['f_network_mult_factor'], params['homophily_weight_range'], params['f_i_factor'], params['r_i_factor'], params['f_opinion'], params['r_opinion'], params['susceptibility'],params['group_opinion_limit_val'],params['group_homophily_limit_val'])
        
    # Not yet done
    
    def test_model_initialization(self):
        print('Function to be implemented')
    
    # Add more tests...

class AgentTests(unittest.TestCase):
    
    def test_commoner_agent(self):
        print('Function to be implemented')
    


class GroupTests(unittest.TestCase):
    
    def test_make_group(self):
        grp = Group(1,75)
        
        self.assertIsInstance(grp, Group)
        self.assertEqual(grp.size, 0)
                
    def test_add_to_group(self):
        grp = Group(2,-75)
        c1 = CommonerAgent(1, 50, -1, 1.2)
        c2 = CommonerAgent(2, 21, -1, 1.4)
        
        grp.join_group(c1)
        grp.join_group(c2)
        
        self.assertEqual(grp.size, 2)
        
    def test_leave_group(self):
        grp = Group(2,-75)
        c1 = CommonerAgent(1, 50, -1, 1.2)
        c2 = CommonerAgent(2, 21, -1, 1.4)
        
        grp.join_group(c1)
        grp.join_group(c2)
        
        self.assertEqual(grp.size, 2)
        
        grp.leave_group(c1)
        
        self.assertNotEqual(grp.size, 2)
        
        grp.leave_group(c2)
        
        self.assertEqual(grp.size, 0)
        
    def test_calculate_avg_opinion(self):
        grp = Group(2,-75)
        c1 = CommonerAgent(1, 25, -1, 1.2)
        c2 = CommonerAgent(2, 75, -1, 1.4)
        c3 = CommonerAgent(3, -25, -1, 1.4)
        grp.join_group(c1)
        grp.join_group(c2)
        
        group_avg_opinion = (c1.opinion+c2.opinion)/2
        self.assertEqual(grp.avg_opinion, group_avg_opinion)
        
        grp.join_group(c3)
        
        self.assertEqual(grp.avg_opinion, 25)
        
        grp.leave_group(c3)
        
        self.assertEqual(grp.avg_opinion, 50)
    
    def test_echo_chamber_limit_value(self):
        # this functionality is basically being mainted by the group class
        
        grp = Group(2,-75) # init value
        c1 = CommonerAgent(1, -80, -1, 1.2)
        c2 = CommonerAgent(2, -90, -1, 1.4)
        c3 = CommonerAgent(2, 17, -1, 1.4)
        grp.join_group(c1)
        grp.join_group(c2)
        
        self.assertEqual(grp.avg_opinion, -85)
        
        grp.join_group(c3)
        
        self.assertNotEqual(grp.avg_opinion, -51.0)
        
        # Since average cannot go below initalization value
        self.assertEqual(grp.avg_opinion, -75)        
       
    def test_polarize(self):
       c1 = CommonerAgent(0, 80, -1, 50)
       c2 = CommonerAgent(1, 90, -1, 60)
        
       grp = Group(1,70)
        
       grp.join_group(c1)
       grp.join_group(c2)
        
       self.assertEqual(grp.avg_opinion,85)
        
       grp.polarize_agents()
       
       self.assertEqual(c1.opinion,85)
       self.assertEqual(c2.opinion,87.5)
       
    # Add more tests

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
        c1 = CommonerAgent(1, -80, -1, 1.2)
        c2 = CommonerAgent(2, -90, -1, 1.4)
        c3 = CommonerAgent(2, 17, -1, 1.4)
        
        agent_list = [c1,c2,c3]
        
        self.assertEqual(agent_list[0].opinion, -80)
        self.assertEqual(agent_list[1].opinion, -90)
        self.assertNotEqual(agent_list[2].opinion, -80)
        
        nodes = make_agent_nodes(agent_list)
        
        for row in nodes:
            self.assertTrue(row[0] == row[1]['agent'].agent_id)
    
    def test_make_agents_connections(self):
        c1 = CommonerAgent(0, -80, -1, 1.2)
        c2 = CommonerAgent(1, -90, -1, 1.4)
        c3 = CommonerAgent(2, 17, -1, 1.4)
        i1 = InfluencerAgent(3, -80, -1, 1, 1.7)
        i2 = InfluencerAgent(4, 80, -1, 0, 1.82)
        
        nodes = [c1,c2,c3,i1,i2]
        edges = make_agents_connections(nodes, 5, 7, 1, 1.6)
        
        for edge in edges:
            a1,a2,w = edge
            if isinstance(a1, CommonerAgent) and isinstance(a2, CommonerAgent):
                self.assertNotEqual(w, 0)
            elif isinstance(a1, InfluencerAgent) and isinstance(a2, CommonerAgent):
                self.assertEqual(w, 0)
        


if __name__ == '__main__':
    unittest.main()
