# Resilient_MTSP
 MTSP solver that is supposed to withstand system failures.


Command to run the code (you need to be in the Resilient_MTSP folder)
python.exe run.py config.txt

In the config file, you can edit the various parameters:

RND_SEED - The random seed to use. This seed will make our results consistent.
TSP_FILE - The .tsp file to use, be sure to include the folder the file is located in.
NUM_ROBS - The number of robots in the scenario.
NUM_SHDS - The number of shutdowns that occur throughout the scenario.
SHD_PROB - The probability of a shutdown occurring at any given timestep.
