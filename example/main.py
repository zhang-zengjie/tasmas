import numpy as np
from utils.config import agent_model, agent_specs
from utils.draw import draw
from utils.functions import config_logger
from components.agent import Agent
from components.assigner import Assigner
import logging, os


def main():

    time_horizon = 25
    space_dim = 2
    num_agents = 4

    model = agent_model(space_dim)
    specs = agent_specs(space_dim, time_horizon)        

    initial_states = [[5, 5], [15, 5], [25, 5], [35, 5]]
    control_bounds = [4, 5, 6, 7]

    agents = {i: Agent(
        model, 
        specs.safety, 
        time_horizon, 
        x0=np.array(initial_states[i]), 
        ub=control_bounds[i], 
        name=i) for i in range(num_agents)}
    TA = Assigner(agents)


    # The list of global specifications

    if not os.path.exists(os.path.join('logs')):
        os.makedirs(os.path.join('logs'))

    config_logger(logging, os.path.join('logs', 'INFO.log'))
    for t in range(time_horizon):

        if t in specs.tlg:
            TA.assign_global(t, specs.slg[specs.tlg.index(t)])
        
        if t in specs.tll:
            TA.assign_local(t, specs.sll[specs.tll.index(t)])
        
        TA.update_control(t)

    measures = {}
    for name, agent in TA.agents.items():
        measures[name] = agent.xx

    draw(measures)


if __name__ == "__main__":

    # Set random seed       
    np.random.seed(3)
    main()
    