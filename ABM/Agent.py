""" File for the Agent class """

class Agent(): 
    def __init__(self, agent_id, opinion, connections):
        """
        superclass for Agent

        Parameters
        ----------
        agent_id : int
            uniqe identifier for each agent.
        opinion : int
            The opinion of the agent - range from -100 to 100
        connections : list<int>
            list of connections, containing ID's of all connected agents.

        Returns
        -------
        None.

        """
        self.agent_id = agent_id
        self.opinion = opinion
        self.connections = connections
        
        
        
class CommonerAgent(Agent): 
    def __init__(self,agent_id, opinion, connections, agent_type, i_susceptibility):
        """
        subclass for commoner agent

        Parameters
        ----------
        agent_type : string
            Signifying the type of agent.
        r_i_susceptibility : int
            how susceptible agent is to be influenced by real news - 0 to 100.
        f_i_susceptibility : int
            how susceptible agent is to be influenced by fake news - -100 to 0.

        Returns
        -------
        None.

        """
        super().__init__(agent_id, opinion, connections)
        self.agent_type = agent_type
        self.r_i_susceptibility = r_i_susceptibility
        self.f_i_susceptibility = f_i_susceptibility



class RInfluencerAgent(Agent):
    def __init__(self,agent_id, opinion, connections, agent_type, i_rate, i_factor):
        """
        Real news influencer agent

        Parameters
        ----------
        agent_type : string
            Signifying the type of agent.
        i_rate : int
            negative value - range from 0 to 100.
        i_factor : int
            effectiveness of influence - range from 0 to 100.

        Returns
        -------
        None.

        """
        super().__init__(agent_id, opinion, connections)
        self.agent_type = agent_type
        self.i_rate = i_rate
        self.i_factor = i_factor



class FInfluencerAgent(Agent):
    def __init__(self,agent_id, opinion, connections, agent_type, i_rate, i_factor):
        """
        Fake news influencer agent

        Parameters
        ----------
        agent_type : string
            Signifying the type of agent.
        i_rate : int
            negative value - range from -100 to 0.
        i_factor : int
            effectiveness of influence - range from 0 to 100.

        Returns
        -------
        None.

        """
        super().__init__(agent_id, opinion, connections)
        self.agent_type = agent_type
        self.i_rate = i_rate
        self.i_factor = i_factor

