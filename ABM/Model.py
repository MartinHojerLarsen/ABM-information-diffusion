# Import statements
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm
from re import I
from Agent import *
import random as rd
from Functions import *
#from Post import *

class Model():
    def __init__(self,population, distribution):
        # Initialize Agent list
        self.agents = []
        # Initialize population
        self.population = population
        # Initialize Graph
        self.graph_environment = nx.Graph()
        
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
    
        
        #Initialize graph environment with agent nodes and edges
        self.graph_environment.add_nodes_from(make_agent_nodes(self.agents))
        self.graph_environment.add_weighted_edges_from(make_agents_connections(self.agents))
    
    def timestep(self):
        nodes_arr = list(self.graph_environment._node.keys())
        rd.shuffle(nodes_arr)
        for agent_id in nodes_arr:
            agent = self.graph_environment._node[agent_id]['agent']
            agent_network = list(self.graph_environment.neighbors(agent_id))
            # Execute influencing process from each individual node to its network
            agent.influence_agent(agent_network)
        
    def update(self):
        raise Exception('Not yet implemented')

    def end(self):
        raise Exception('Not yet implemented')

# =============================================================================
# Testing environment
# =============================================================================
model = Model(7,(70,30))
draw_graph_environment(model)
# Timestep still in test phase
model.timestep()

print('[+] Execution done')
