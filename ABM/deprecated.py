""" Deprecated code pieces """

# =============================================================================
#     Agent methods
# =============================================================================
    # def check_homophily(self, target, graph_env):
    #     """
    #     Check the homophily relationship between self and target agent

    #     Parameters
    #     ----------
    #     target : Agent
    #         target agent to check homophily with.
    #     graph_env : networkx graph
    #         Graph dataset to find edge_weights(homophily) from

    #     Returns
    #     -------
    #     Boolean
    #         True if homophily between self and target > 1.2 (value can be altered).
    #         False otherwise. 
    #     """
    #     homophily = graph_env.get_edge_data(self.agent_id,target.agent_id)['weight']
        
    #     # a limit to when a friendship is good enough to create groups
    #     limit_value = 1.2
        
    #     return homophily > limit_value 
    
    # def send_group_invite(self, target, global_groups, graph_env):
    #     """
    #     Send group invitation to target (agent).
    #     Checks global group list to not create duplicate group IDs. 

    #     Parameters
    #     ----------
    #     target : Agent
    #         Agent object - the target of invitation.
    #     global_group_ids : list
    #         list of group IDs to check (ensuring no duplicate groups)

    #     Returns
    #     -------
    #     None.

    #     """
    #     # check homophily and opinion. If true -> send_invite()
    #     if self.check_homophily(target, graph_env) and self.check_opinion(target):
            
    #         # create agent object from graph_env ### MAKE SURE THAT THIS UPDATES ON IN GRAPH ENV (reference pointers)
    #         agent_instance = graph_env._node[self.agent_id]['agent']
    #         # create new group object
    #         new_group = Group(self.group_id, 1, [agent_instance])
    #         # if group ID is taken OR not assigned
    #         if self.group_id in global_groups or self.group_id == -1:
    #             # create new group ID 
    #             self.group_id = len(global_groups)
                
    #             global_groups[self.group_id] = {self.group_id: new_group}
    #             target.group_invites.append((self.group_id, self.agent_id))
    #         else:
    #             # send invite            
    #             global_groups[self.group_id] = {self.group_id: new_group}
    #             target.group_invites.append((self.group_id, self.agent_id))
    
    
