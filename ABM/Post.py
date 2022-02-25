# File for post object/class

class Post(): 
    """
        class for Post

        Parameters
        ----------
        id : int
            uniqe identifier for each post.
        opinion : int
            The opinion of the post - range from -100 to 100
        connections : list<int>
            list of agents that the post is "active" on

        """
    def __init__(self, ID, opinion): 
        self.ID = ID
        self.opinion = opinion
        self.connections = []

        def add_connection(self, ID): 
            self.connections.add(ID)

        def remove_connection(self, ID):
            self.connections.remove(ID)
        
        def all_connections(self): 
            return self.connections


a = Post(0, 12)
a.add_connection(2)

print(a.all_connections())
