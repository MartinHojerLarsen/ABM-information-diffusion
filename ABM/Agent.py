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
        self.agent_connections = connections
        
class CommonerAgent(Agent): 
    def __init__(self,agent_id, opinion, connections, i_susceptibility):
        """
        subclass for commoner agent

        Parameters
        ----------
        agent_type : string
            Signifying the type of agent.
        i_susceptibility : int
            how susceptible agent is to be influenced by real news - -100 to 100.

        Returns
        -------
        None.

        """
        super().__init__(agent_id, opinion, connections)
        self.i_susceptibility = i_susceptibility


class InfluencerAgent(Agent):
    def __init__(self,agent_id, opinion, connections, agent_type, i_rate, i_factor):
        """
        Subclass for influencer agent

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

