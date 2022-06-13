import Model
import time
import pandas as pd
from Functions import *
# ============================================================================= #
#                            Model Execution section                            #
# ============================================================================= #

# Benchmarking
start = time.time() # Used to track performance of the model

### Parameters ###
params = {
    'timesteps': 500, # declare amount of timesteps
    "population": 500, # declare the overall population of the ABM
    "population_distribution":(80, 10, 10), # percentages: user, fake, real
    "user_network": 4, # how many connections should a typical user have
    "influencer_network": 7, # how many connections should a typical influencer have
    "finfluencer_network_mult_factor": 1, # starts at 1 - a multiplication of fake news influencer network - due to fake news spreading more
    "homophily_weight_range": 2, # homophily between users
    "f_influence_factor": (1, 2), # influence factor - fake news influencer (should be higher for Finfluencer)
    "r_influence_factor": (1, 2), # influence factor - real news influencer
    "f_opinion": (-100, -50), #  range of opinion - fake news influencer (should be more radical for Finfluencer)
    "r_opinion": (50, 100), # range of opinion - real news influencer
    "user_susceptibility": (1, 2), # susceptibility - user - random value between 1 and 2
    'echo_chamber_entrance_limit': 5, # determine the limit for when a opinion should reflect a potential join of an echo chamber
    'echo_chamber_homophily_limit': 1.5 # determine the homophily between agents that should be in an echo chamber
}

### Settings ###
# Specify whether to draw the graph of the model
draw_graph = True
# Specify whether output the results into excel files
create_excel_files = False
# Specify how many times the model should run
model_iterations = 1
##################

# Model iterations
df_global_dataframes = []
df_groups_dataframes = []
df_individual_agents_dataframes = []
for j in range(model_iterations):
    # Create model
    model = Model.Model(params['population'], params['population_distribution'], params['user_network'], params['influencer_network'], params['finfluencer_network_mult_factor'], params['homophily_weight_range'], params['f_influence_factor'], params['r_influence_factor'], params['f_opinion'], params['r_opinion'], params['user_susceptibility'],params['echo_chamber_entrance_limit'],params['echo_chamber_homophily_limit'])
    
    # run simulations for amount of timestep specified in the parameter list
    for i in range(params['timesteps']):
        model.timestep()
    
    # Create a pandas dataframe with the final global opinion values
    model.finalize_model()
    
    # Append a singular model iteration to a list of dataframe for agents, groups and global opinion
    df_individual_agents_dataframes.append(model.dataset_individual_agent)
    df_groups_dataframes.append(model.dataset_groups)
    df_global_dataframes.append(model.dataset_global_opinion)

# Gather all episodes into one dataframe for agents, groups and global opinion.
df_global = pd.concat(df_global_dataframes,axis=1)
df_groups = pd.concat(df_groups_dataframes,axis=1)
df_agents = pd.concat(df_individual_agents_dataframes,axis=1)

done = time.time() # Used to track performance of the model
elapsed = done - start # Used to track performance of the model
print(f'Model running time: {elapsed}s')

# Draw graph
if draw_graph:
    draw_graph_environment(model)

if create_excel_files:
    #=============================================================================
    # Create excel files
    #=============================================================================
    writer_start = time.time()
    writer = pd.ExcelWriter('../Data/SC2_echo_chamber_1_3.xlsx', engine='openpyxl')
    # # Convert the dataframe to an XlsxWriter Excel object.
    df_global.to_excel(writer, sheet_name='global', index=False)
    print("Global done")
    df_groups.to_excel(writer, sheet_name='groups', index=False)
    print("Groups done")
    df_agents.to_excel(writer, sheet_name='agents', index=False)
    # # Close the Pandas Excel writer and output the Excel file.
    print("Agents done")
    writer.save()
    writer.close()
    print("Writer closed")
    writer_done = time.time()
    writer_time = writer_done - writer_start
    print(f'Writer running Time: {writer_time}')
    print("Finished run")