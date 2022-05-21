""" File for Group class """
from Agent import UserAgent
from Agent import InfluencerAgent

class Group(): 
    def __init__(self, group_id,limit_value):
        self.group_id = group_id
        self.size = 0
        self.agent_list = []
        self.avg_opinion = 0
        self.limit_value = limit_value
        

    def calc_avg_opinion(self):
        """
        Calculate the average opinion of the given group.
    
        Returns
        -------
        average : int
            Average of all agent opinions in group list.
    
        """
        opinion_sum = 0
        
        if len(self.agent_list) == 0:
            return
        
        for agent in self.agent_list:
            opinion_sum += agent.opinion

        average = opinion_sum/len(self.agent_list)
                
        # Ensure that echo chambers cannot be in the range of the positive range of the limit value.
        if -abs(self.limit_value) <= average <= abs(self.limit_value):
            self.avg_opinion = self.limit_value
        else:
            self.avg_opinion = average
        
    def join_group(self, agent):
        """
        Function for an Agent to join the group 
        Uses calc_avg_opinion()

        Parameters
        ----------
        agent : Agent
            Agent to join the group.

        Returns
        -------
        None.

        """
        self.size += 1
        self.agent_list.append(agent)
        self.calc_avg_opinion()
        agent.group_id = self.group_id
        
    def leave_group(self, agent): 
        """
        Function for an Agent to leave the group
        Uses calc_avg_opinion()
        Parameters
        ----------
        agent : Agent
            Agent to leave the group.

        Returns
        -------
        None.

        """
        self.size -= 1
        self.agent_list.remove(agent)
        self.calc_avg_opinion()
        agent.group_id = -1
        
    def polarize_agents(self):
        """
        A method to polarize all agents in a given group closer to the groups average opinion.
        Simulates the tendencies of an echo chamber.

        Returns
        -------
        None.

        """
        for agent in self.agent_list:
            
            if isinstance(agent,UserAgent):
                opinion_variance = abs(agent.opinion-(self.avg_opinion)) 
                if opinion_variance < 1:
                    opinion_variance = 1
                
                # state to make proper calculation if agent has a positive or negative opinion
                state = 'not defined'
                if agent.opinion < self.avg_opinion:
                    state = 'add'
                elif agent.opinion > self.avg_opinion:
                    state = 'subtract'
                else:
                    state = 'equal'
                
                # opinion calculation (value is higher the closer the agent opinion is as global opinion)
    
                opinion_calculation = abs((1/opinion_variance)*agent.opinion)
    
                    
                if state == 'add':
                    new_opinion = agent.opinion + opinion_calculation # polarize towards global opinion
                    # agent opinion cannot exceed global opinion 
                    if new_opinion > self.avg_opinion:
                        new_opinion = self.avg_opinion
                elif state == 'subtract':
                    new_opinion = agent.opinion - opinion_calculation # polarize towards global opinion
                    # agent opinion cannot exceed global opinion
                    if new_opinion < self.avg_opinion:
                        new_opinion = self.avg_opinion
                else:
                    new_opinion = agent.opinion
                    
                agent.opinion = new_opinion
                # calculate new average opinion of the group
                self.calc_avg_opinion()


