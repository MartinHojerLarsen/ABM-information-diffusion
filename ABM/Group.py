""" File for Group class """
from Agent import CommonerAgent

class Group(): 
    def __init__(self, group_id,echo_chamber_limit_value):
        self.group_id = group_id
        self.size = 0
        self.agent_list = []
        self.avg_opinion = 0
        self.echo_chamber_limit_value = echo_chamber_limit_value
        

    def calc_avg_opinion(self):
        """
        return average opinion of all agents in agent_list
    
        Parameters
        ----------
        agent_list : list<agent>
            List of agents.
    
        Returns
        -------
        average : int
            Average of all agent opinions in input list.
    
        """
        opinion_sum = 0
        num_state = 'zero'
        
        for agent in self.agent_list:
            opinion_sum += agent.opinion
            
        average = opinion_sum/len(self.agent_list) if len(self.agent_list) != 0 else 0
        
        # Ensure that echo chambers cannot be in the range of -50 <=> 50.
        if opinion_sum < 0:
            num_state = 'n'
        elif opinion_sum == 0:
            num_state = 'zero'
        elif opinion_sum > 0:
            num_state = 'p'
        
        if num_state == 'n' and average > self.echo_chamber_limit_value:
            self.avg_opinion = self.echo_chamber_limit_value
        elif num_state == 'p' and average < self.echo_chamber_limit_value:
            self.avg_opinion = self.echo_chamber_limit_value
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
        for agent in self.agent_list:
            opinion_variance = abs(agent.opinion-self.avg_opinion) if (agent.opinion-self.avg_opinion) != 0 else 1
            
            # state to make proper calculation if agent has a positive or negative opinion
            state = 'not defined'
            if agent.opinion < self.avg_opinion:
                go_state = 'add'
            elif agent.opinion > self.avg_opinion:
                go_state = 'subtract'
            else:
                go_state = 'equal'
            
            # opinion calculation (value is higher the closer the agent opinion is as global opinion)

            opinion_calculation = abs((1/opinion_variance)*agent.opinion)

                
            if go_state == 'add':
                new_opinion = agent.opinion + opinion_calculation # polarize towards global opinion
                # agent opinion cannot exceed global opinion 
                if new_opinion > self.avg_opinion:
                    new_opinion = self.avg_opinion
            elif go_state == 'subtract':
                new_opinion = agent.opinion - opinion_calculation # polarize towards global opinion
                # agent opinion cannot exceed global opinion
                if new_opinion < self.avg_opinion:
                    new_opinion = self.avg_opinion
            else:
                new_opinion = agent.opinion
                
            agent.opinion = new_opinion
            # calculate new average opinion of the group
            self.calc_avg_opinion()

# =============================================================================
# TESTING 
# =============================================================================

c1 = CommonerAgent(0, 80, -1, 50)
c2 = CommonerAgent(1, 90, -1, 60)

grp = Group(1,70)

grp.join_group(c1)
grp.join_group(c2)

grp.polarize_agents()


