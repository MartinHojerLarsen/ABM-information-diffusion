# Agent-based Model of How Misinformation Spreads in a Social Network.

## Introduction
This repository includes all the code for Mads and Martin's Master Thesis. 

The project is about developing (with existing tools) an Agent Based Model of information diffusion in a social network. 
We want to investigate the relation and dynamics between agents, group formation and the network as a whole, and, how real news and fake news influence agents choice of recieving the vaccine for Covid-19 or not. 

We are investigating this through Multiscale systems, information diffusion theory, based on an Agent Based Model. 
Agents in the system include commoner, fake news influencer and real news influencer.

## Installation
In order for the system to work. The following packages must be installed.
```bash
pip install networkx
pip install matplotlib
pip install openpyxl
pip install pandas
pip install numpy
```

## Usage
In order to use the model, it is possible to modify the values given in the parameter list below.

The following parameter list is an example of how to initialize the model.

```bash
    ### Parameters ###
    params = {
        'timesteps': 100,
        "population": 30, 
        "population_distribution":(80, 10, 10), 
        "user_network": 4, 
        "influencer_network": 7, 
        "finfluencer_network_mult_factor": 1,
        "homophily_weight_range": 2,
        "f_influence_factor": (1, 2),
        "r_influence_factor": (1, 2), 
        "f_opinion": (-100, -50), 
        "r_opinion": (50, 100), 
        "user_susceptibility": (1, 2), 
        'echo_chamber_entrance_limit': 5, 
        'echo_chamber_homophily_limit': 1.5 
    }
```
There are various opportunities to alter the values of the parameters in the model. In the following a short description of each parameter will be elaborated.

**Timesteps**
Specify the amount of ticks/timesteps that the model should run. Timesteps can be seen as the amount of time that passes inside the model.

Given as an arbitrary integer

**Population**
Specify how many agents should be in the Model. Be aware of potential performance issues of having a very large population.

Given as an arbitrary integer

**Population Distribution**
Determines the percentage of UserAgents, Finfluencer agents and Rinfluencer agents in the system. This value is given a triple and must equal 100% in all

the format is (percentage of userAgents, percentage of Rinfluencer, percentage of Finfluencer)

Example
(50,25,25) Valid
(25,25,50) Valid
(10,10,33) Invalid

Given as a triple of integers

**User Network**
Specify the approximate amount of connections a singular UserAgent has. The exact amount of friends can vary due to specific circumstances.

Given as an arbitrary integer.

**Influencer Network**
Specify the network size of the Rinfluencer and Finfluencer

Given as an arbitrary integer.

**Finfluencer network multiplication factor**
Despite a bad variable name... the following specified factor will increase the Finfluencer network more than the Rinfluencer network.

Given as an arbitrary integer.

**Homophily weight range**
Specify the range value in which UserAgents can establish a homophily relationship between each other.

Given as a tuple of floats from 1 <=> 2.

**F influence factor**
Specify how good Finfluencer are at influencing UserAgents.

Given as a tuple of floats from 1 <=> 2.

**R influence factor**
Specify how good Rinfluencer are at influencing UserAgents.

Given as a tuple of floats from 1 <=> 2.

**F opinion**
Specify the opinion range in which Finfluencers can be initialized. The value are typically in the range of -75 <=> -100.

Given as a tuple of integers

**R opinion**
Specify the opinion range in which Rinfluencers can be initialized. The value are typically in the range of 75 <=> 100.

Given as a tuple of integers from -100 <=> 100.

**User susceptibility**
Specify a range, determining how susceptibel UserAgents are towards being influenced by Rinfluencers or Finfluencers.

Given as a tuple of floats from 1 <=> 2.

**Echo Chamber Entrance Limit**
Specify how similar the agent's opinions should be in order to establish/join an echo chambers. Low value => low probability of establishment, High value => High probability of establishment

given as an arbitrary integer.

**Echo chamber Homophily Limit**
Specify how good of a relationship UserAgents should have in order to potentially establish/join an echo chambers. Higher value => low probability of establishment, Low value => High probability of establishment.

Given as an float of 1 <=> 2.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
