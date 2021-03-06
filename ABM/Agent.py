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
            unique identifier for current group. Default is -1. 

        Returns
        -------
        None.

        """
    
        self.agent_id = agent_id
        self.opinion = opinion
        self.group_id = group_id
        
    
class UserAgent(Agent): 
    def __init__(self,agent_id, opinion, group_id, i_susceptibility):
        """
        subclass for Agent.
        Inherits the same attributes as the parent class.

        Parameters
        ----------
        i_susceptibility : float
            how susceptible agent is to be influenced by real news (1 to 2).

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
            Input a networkx graph - nx.Graph()
        list_of_neighbors : List of integers
            Takes a list of integers represented as unique ids
        SCALE_DOWN_FACTOR : int, optional
            Used to scale down the influencing factor, so the agent opinion will not be to high and unreadable. The default is 60.
        
        Returns
        -------
        Nothing

        """
        
        for agent_id in list_of_neighbors:
            # current node to influence
            target_agent = graph_env._node[agent_id]['agent']
            if isinstance(target_agent,InfluencerAgent) == True:
                continue
            else:
                # current nodes opinion
                target_agent_opinion = target_agent.opinion
                # current nodes susceptibility
                target_agent_susceptibility = target_agent.i_susceptibility 
                if target_agent_susceptibility == 1:
                    target_agent_susceptibility = 0 
                
                # calculate new target opinion
                if (self.opinion >= 0 and target_agent_opinion >= 0) or (self.opinion < 0 and target_agent_opinion < 0):
                    similar_mindset = 1.5 
                else: 
                    similar_mindset = 1
                
                opinion_variance = abs(self.opinion-(target_agent_opinion)) 
                if opinion_variance < 1: 
                    opinion_variance = 1
                
                opinion_difference = 1/opinion_variance
                homophily = graph_env.get_edge_data(self.agent_id,target_agent.agent_id)['weight']
                
                if self.opinion >= 0:
                    target_new_opinion = target_agent_opinion+(opinion_difference*target_agent_susceptibility*similar_mindset*homophily)/SCALE_DOWN_FACTOR
                else:
                    target_new_opinion = target_agent_opinion-(opinion_difference*target_agent_susceptibility*similar_mindset*homophily)/SCALE_DOWN_FACTOR
                
                # Make boundaries for degree of opinion
                if target_agent_opinion >= 100:
                    target_new_opinion = 100
                elif target_new_opinion <= -100:
                    target_new_opinion = -100
                else:
                    target_new_opinion
                
                target_agent.opinion = target_new_opinion
                
    def global_opinion_reflection(self,global_opinion_val):
        """
        A method for an individual userAgent to reflect upon the global opinion provided in the ABM.

        Parameters
        ----------
        global_opinion_val : int
            Takes an integer represented as the current global opinion value at a given timestep.

        Returns
        -------
        None.

        """
        
        # difference in agent opinion and current timesteps global opinion
        go_variance = abs(self.opinion-(global_opinion_val)) 
        if go_variance < 1:
            go_variance = 1
        
        # state to make proper calculation if agent has a positive or negative opinion
        go_state = 'not defined'
        if self.opinion < global_opinion_val:
            go_state = 'add'
        elif self.opinion > global_opinion_val:
            go_state = 'subtract'
        else:
            go_state = 'equal'
        
        # opinion calculation (value is higher the closer the agent opinion is as global opinion)
        opinion_calculation = abs((1/go_variance)*self.opinion)

        if go_state == 'add':
            # absolute difference is less than 50 - then polarize towards GO (explain in DOCS)
            # if absolute difference is MORE than 50 - then oppposite effect (away from GO)
            if go_variance < 50:
                new_opinion = self.opinion + opinion_calculation # polarize towards global opinion
            else:
                new_opinion = self.opinion - opinion_calculation # polarize away from global opinion
            
            # agent opinion cannot exceed global opinion 
            if new_opinion > global_opinion_val:
                new_opinion = global_opinion_val
        elif go_state == 'subtract':
            if go_variance < 50:
                new_opinion = self.opinion - opinion_calculation # polarize towards global opinion
            else:
                new_opinion = self.opinion + opinion_calculation # polarize away from global opinion
            
            # agent opinion cannot exceed global opinion
            if new_opinion < global_opinion_val:
                new_opinion = global_opinion_val
        elif go_state == 'equal':
            new_opinion = global_opinion_val

        self.opinion = new_opinion

class InfluencerAgent(Agent):
    def __init__(self,agent_id, opinion, group_id, agent_type, i_factor):
        """
        Subclass for Agent.
        Inherits the same attributes as the parent class.

        Parameters
        ----------
        agent_type : int
            Signifying the type of agent. 0 = Real news, 1 = Fake news
        i_factor : float
            effectiveness of influence - range from (1 to 2).

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
            Used to scale down the influencing factor, so the agent opinion will not be to high and unreadable. The default is 80.

        Returns
        -------
        Nothing

        """
        for agent_id in list_of_neighbors:
            # current node to influence
            target_agent = graph_env._node[agent_id]['agent']
            # current nodes opinion
            target_agent_opinion = target_agent.opinion
            
            # current nodes susceptibility
            target_agent_susceptibility = target_agent.i_susceptibility 
            if target_agent_susceptibility == 1:
                target_agent_susceptibility = 0 
            
            # calculate new target opinion
            if (self.opinion >= 0 and target_agent_opinion >= 0) or (self.opinion < 0 and target_agent_opinion < 0):
                similar_mindset = 1.5 
            else: 
                similar_mindset = 1
                
            ifs_factor = self.i_factor * target_agent_susceptibility
            
            opinion_variance = abs(self.opinion-(target_agent_opinion)) 
            if opinion_variance < 1: 
                opinion_variance = 1    
            
            opinion_difference = 1/opinion_variance 
            
            if self.opinion >= 0:
                target_new_opinion = target_agent_opinion + (opinion_difference * ifs_factor * similar_mindset) / SCALE_DOWN_FACTOR
            else:
                target_new_opinion = target_agent_opinion - (opinion_difference * ifs_factor * similar_mindset) / SCALE_DOWN_FACTOR
            # Make boundaries for degree of opinion
            if target_agent_opinion >= 100:
                target_new_opinion = 100
            elif target_new_opinion <= -100:
                target_new_opinion = -100
            else:
                target_new_opinion
            
            target_agent.opinion = target_new_opinion
            
            
