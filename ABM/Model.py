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
        self.graph_environment = nx.Graph()
        
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
    
        
        #Initialize graph environment with agent nodes and edges
        self.graph_environment.add_nodes_from(make_agent_nodes(self.agents))
        self.graph_environment.add_edges_from(make_agents_connections(self.agents))
    
    def timestep(self):
        nodes_arr = list(model.graph_environment._node.keys())
        rd.shuffle(nodes_arr)
        for agent in nodes_arr:
            agent_network = list(model.graph_environment.neighbors(agent))
            ## Init agent method on all adjacent edges
        raise Exception ('In progress')
        
    def update(self):
        raise Exception('Not yet implemented')

    def end(self):
        raise Exception('Not yet implemented')



# =============================================================================
# Testing environment
# =============================================================================
model = Model(30,(65,35))
draw_graph_environment(model)

# model.timestep()

print('[+] Execution done')
