# Import statements
from re import I
from Agent import *
from Functions import *
#from Post import *


class Model():
    def __init__(self,population, distribution):
        # Initialize Agent list
        self.agents = []
        # Initialize population
        self.population = population
        commoner_dist,influencer_dist = distribution
        if commoner_dist + influencer_dist != 100:
            raise Exception("Population distribution mismatch. Must be equal to 100")

        self.commoner_population = round(self.population*(commoner_dist/100)) # Divides population into Commoners and Influencers
        self.influencer_population = round(self.population*(influencer_dist/100)) # Divides population into Commoners and Influencers

        for i in range(0,self.commoner_population):
            agent_id = i
            agent_opinion = rd.randint(-100, 100)
            random_connection_list = make_connection_list(i,self.population)
            i_susceptibility = rd.randint(0, 100)

            self.agents.append(CommonerAgent(agent_id,agent_opinion,random_connection_list,i_susceptibility))

        for i in range(self.commoner_population,self.population):
            agent_id = i
            agent_opinion = rd.randint(-100, 100)
            random_connection_list = make_connection_list(i,self.commoner_population,True)
            influencer_type = rd.randint(0,1) # 0 = Real News, 1 = Fake News

            # OBS!! These might be moved to the post object
            i_rate = rd.randint(-100,100)
            i_factor = rd.randint(-100, 100)
            self.agents.append(InfluencerAgent(agent_id,agent_opinion,random_connection_list,influencer_type,i_rate,i_factor))

# Testing section
model = Model(30,(80,20))

print('end')