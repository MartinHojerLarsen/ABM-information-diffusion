# Import statements
from re import I
from Agent import *
import random as rd
from Functions import *
import networkx as nx
#from Post import *

class Model():
    def __init__(self,population, distribution):
        # Initialize Agent list
        self.agents = []
        # Initialize population
        self.population = population
        # Initialize Graph
        self.graph = nx.Graph()
        
        commoner_dist,influencer_dist = distribution
        if commoner_dist + influencer_dist != 100:
            raise Exception("Population distribution mismatch. Must be equal to 100")

        self.commoner_population = round(self.population*(commoner_dist/100)) # Divides population into Commoners and Influencers
        self.influencer_population = round(self.population*(influencer_dist/100)) # Divides population into Commoners and Influencers

        for i in range(0,self.commoner_population):
            # create commoner agents
            agent_id = i
            agent_opinion = rd.randint(-100, 100)
            i_susceptibility = rd.randint(0, 100)

            self.agents.append(CommonerAgent(agent_id,agent_opinion,i_susceptibility))

        for i in range(self.commoner_population,self.population):
            # create influencer agents
            agent_id = i
            agent_opinion = rd.randint(-100, 100)
            influencer_type = rd.randint(0,1) # 0 = Real News, 1 = Fake News

            # OBS!! These might be moved to the post object
            # =============================================================================
            i_rate = rd.randint(-100,100)
            i_factor = rd.randint(-100, 100)
            # =============================================================================
            self.agents.append(InfluencerAgent(agent_id,agent_opinion,influencer_type,i_rate,i_factor))
    
        # Initialize graph network between agents
        self.graph.add_nodes_from(self.agents)
        self.agent_connections = make_agents_connections(self.agents)
        self.graph.add_edges_from(self.agent_connections)
    
    def timestep():
        raise Exception('Not yet implemented')

    def update():
        raise Exception('Not yet implemented')

    def end():
        raise Exception('Not yet implemented')

# =============================================================================
# Testing environment
# =============================================================================

model = Model(3000,(75,25))
nx.draw(model.graph)
print('[+] Execution done')