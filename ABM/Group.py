""" File for Group class """
class Group(): 
    def __init__(self, group_id, opinion_start, opinion_end):

        self.group_id = group_id
        self.opinion_start = opinion_start
        self.opinion_end = opinion_end
        self.size = 0
        self.agent_list = []
        self.avg_opinion = 0


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
        for agent in self.agent_list:
            opinion_sum += agent.opinion
            
        average = opinion_sum/len(self.agent_list)
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
        

# =============================================================================
# TESTING 
# =============================================================================
# c1 = CommonerAgent(0, -95, -1, 50)
# c2 = CommonerAgent(1, -88, -1, 60)

# g = Group(0, -100, -90)

# if c2.check_opinion(g):
#     g.join_group(c1)
#     print("joined group")

# if c1.check_opinion(g):
#     g.join_group(c1)
#     print("joined group")
