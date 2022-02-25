# This file is used to define isolated functions for our ABM
import doctest
import random as rd
import math

def make_connection_list(agent_id,population,influencerList = False):
    """A function that creates a connection between agents.

    Parameters
    ----------
    agent_id : integer
        Takes an Agent id
    population : integer
        Define agent population

    Returns
    -------
    List of integer
        Return a list of integers represented as agent ids
    """

    # Make a single agent to have at least 1 or 2 connections (could be improved in the future)
    if influencerList:
        singular_set = set(rd.sample(range(0, population), rd.randint(math.ceil(population/2),population))) 
    else:
        singular_set = set(rd.sample(range(0, population), rd.randint(2,population)))
    singular_list = list(singular_set)
    if agent_id in singular_list:
        singular_list.remove(agent_id)
    return singular_list

print(make_connection_list(3,10))

