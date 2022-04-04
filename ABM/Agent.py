""" File for the Agent class """

class Agent(): 
    def __init__(self, agent_id, opinion, group_id=-1):
        """
        superclass for Agent

        Parameters
        ----------
        agent_id : int
            uniqe identifier for each agent.
        opinion : int
            The opinion of the agent - range from -100 to 100
        group_id : int
            unique identifier for current group 

        Returns
        -------
        None.

        """
    
        self.agent_id = agent_id
        self.opinion = opinion
        self.group_id = group_id
        
    
class CommonerAgent(Agent): 
    def __init__(self,agent_id, opinion, group_id, i_susceptibility):
        """
        subclass for commoner agent

        Parameters
        ----------
        agent_type : string
            Signifying the type of agent.
        i_susceptibility : float
            how susceptible agent is to be influenced by real news - 1 to 2.

        Returns
        -------
        None.

        """
        super().__init__(agent_id, opinion, group_id)
        self.i_susceptibility = i_susceptibility
        
    def influence_agent(self,graph_env,list_of_neighbors,SCALE_DOWN_FACTOR = 60):
        """
        The following method is going through a network of agent and then influence them by certain factors.
        These factors are homophily, susceptibility, influence factor and opinion.

        Parameters
        ----------
        graph_env : networkx graph
            Input a network x graph - nx.Graph()
        list_of_neighbors : List of integers
            Takes a list of integers represented as unique ids
        SCALE_DOWN_FACTOR : int, optional
            Used to scale down the influencing factor, so the agent opinion will not be to high and unreadable. The default is 60.

        Returns
        -------
        Nothing

        """
        
        # print(f'#####################')
        # print(f'###Agent (Commoner) Opinion: {self.opinion}###')
        # print(f'#####################')
        for agent_id in list_of_neighbors:
            # current node to influence
            target_agent = graph_env._node[agent_id]['agent']
            if isinstance(target_agent,InfluencerAgent) == True:
                continue
            else:
                # current nodes opinion
                target_agent_opinion = target_agent.opinion
                # current nodes susceptibility
                target_agent_susceptibility = target_agent.i_susceptibility if target_agent.i_susceptibility != 1 else 0 
                # calculate new target opinion
                similar_mindset = 1.5 if (self.opinion >= 0 and target_agent_opinion >= 0) or (self.opinion < 0 and target_agent_opinion < 0) else 1
                opinion_difference = self.opinion-target_agent_opinion # This is up for discussion
                homophily = graph_env.get_edge_data(self.agent_id,target_agent.agent_id)['weight']
                # print(f'Homophily between agents {homophily}')
                
                target_new_opinion = target_agent_opinion+(opinion_difference*target_agent_susceptibility*similar_mindset*homophily)/SCALE_DOWN_FACTOR
                
                # Make boundaries for degree of opinion
                if target_agent_opinion >= 100:
                    target_new_opinion = 100
                elif target_new_opinion <= -100:
                    target_new_opinion = -100
                else:
                    target_new_opinion
                
                target_agent.opinion = target_new_opinion

class InfluencerAgent(Agent):
    def __init__(self,agent_id, opinion, group_id, agent_type, i_factor):
        """
        Subclass for influencer agent

        Parameters
        ----------
        agent_type : string
            Signifying the type of agent.
        i_factor : float
            effectiveness of influence - range from 1 to 2.

        Returns
        -------
        None.

        """
        super().__init__(agent_id, opinion, group_id)
        self.agent_type = agent_type
        self.i_factor = i_factor
        
    def influence_agent(self,graph_env,list_of_neighbors,SCALE_DOWN_FACTOR = 80):
        """
        The following method is going through a network of agent and then influence them by certain factors.
        These factors are homophily, susceptibility, influence factor and opinion.

        Parameters
        ----------
        graph_env : networkx graph
            Input a network x graph - nx.Graph()
        list_of_neighbors : List of integers
            Takes a list of integers represented as unique ids
        SCALE_DOWN_FACTOR : int, optional
            Used to scale down the influencing factor, so the agent opinion will not be to high and unreadable. The default is 60.

        Returns
        -------
        Nothing

        """
        # print(f'#####################')
        # print(f'###Agent (Influence){self.opinion}###')
        # print(f'#####################')
        for agent_id in list_of_neighbors:
            # current node to influence
            target_agent = graph_env._node[agent_id]['agent']
            # current nodes opinion
            target_agent_opinion = target_agent.opinion
            # current nodes susceptibility
            target_agent_susceptibility = target_agent.i_susceptibility if target_agent.i_susceptibility != 1 else 0 
            # calculate new target opinion
            similar_mindset = 1.5 if (self.opinion >= 0 and target_agent_opinion >= 0) or (self.opinion < 0 and target_agent_opinion) < 0 else 1
            ifs_factor = self.i_factor * target_agent_susceptibility
            opinion_difference = self.opinion - target_agent_opinion
            
            
            target_new_opinion = target_agent_opinion + (opinion_difference * ifs_factor * similar_mindset) / SCALE_DOWN_FACTOR
            
            # Make boundaries for degree of opinion
            if target_agent_opinion >= 100:
                target_new_opinion = 100
            elif target_new_opinion <= -100:
                target_new_opinion = -100
            else:
                target_new_opinion
            
            # embed new opinion
            # print(f'target opinion: {target_agent_opinion}')
            target_agent.opinion = target_new_opinion
            # print(f'target new opinion: {target_agent.opinion}')
            # print('')
            
            
